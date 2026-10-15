"""MCP tool loader for fleet-deepagents-export.

Builds MCP server connections for tools listed in a Fleet export. Each
tool's ``mcp_server_url`` is resolved against LangSmith's registry, and
one of three auth paths is taken:

- **Builtin LangSmith tool server** (matches ``BUILTIN_MCP_URL`` hostname):
  connects with ``X-Api-Key`` + ``X-Auth-Scheme: langsmith-api-key`` plus
  ``X-Tenant-Id`` / ``X-Organization-Id`` / ``X-Ls-User-Id`` for OAuth-backed
  tools like Gmail/Calendar.
- **Registered with ``auth_type: "headers"``** (via
  ``GET /v1/platform/fleet/mcp-servers`` on smith-backend): headers come
  from the registry record.
- **Registered with ``auth_type: "oauth"``**: bearer token fetched via
  ``POST /v2/auth/authenticate`` on host-backend (``api.host.langchain.com``,
  a separate service) using the server's ``oauth_provider_id``.

Servers that can't be resolved or authed are skipped with a warning.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import webbrowser
from datetime import timedelta
from urllib.parse import urlparse

import httpx
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger(__name__)

DEFAULT_LANGSMITH_HOST = "https://api.smith.langchain.com"
DEFAULT_HOST_BACKEND_URL = "https://api.host.langchain.com"
OAUTH_POLL_SECONDS = 120

# Serializes the interactive browser/poll consent flow so concurrent
# connection resolution can't open multiple consent tabs at once.
_OAUTH_BROWSER_LOCK = asyncio.Lock()


async def build_connections(tool_entries: list[dict]) -> dict[str, dict]:
    """Build MCP server connections by resolving each URL against LangSmith."""
    # Unique URLs referenced by the export (case-insensitive, trailing-slash normalized)
    unique_urls: dict[str, str] = {}
    for tool in tool_entries:
        url = (tool.get("mcp_server_url") or "").rstrip("/")
        if url:
            unique_urls.setdefault(url.lower(), url)

    if not unique_urls:
        return {}

    # Only fetch the MCP server registry if we reference any non-builtin URL
    needs_registry = any(not _is_builtin_server(u) for u in unique_urls.values())
    registry_by_url: dict[str, dict] = {}
    if needs_registry:
        for server in await _list_mcp_servers():
            norm = _normalize_url(server.get("url"))
            if norm:
                registry_by_url[norm] = server

    # Resolve all URLs concurrently; gather preserves order, so the
    # disambiguation counter below stays deterministic.
    items = list(unique_urls.items())
    resolved = await asyncio.gather(
        *(
            _connection_for(original_url, registry_by_url.get(norm_url))
            for norm_url, original_url in items
        )
    )

    connections: dict[str, dict] = {}
    for conn in resolved:
        if conn is None:
            continue
        name, spec = conn
        # Two distinct servers can sanitize to the same name (duplicate display
        # names, or two hosts that both fall back to the same URL-derived key).
        # Disambiguate by appending a counter so neither connection is dropped.
        if name in connections:
            base = name
            counter = 2
            while name in connections:
                name = f"{base}-{counter}"
                counter += 1
        connections[name] = spec

    return connections


async def fetch_server_tools(
    client: MultiServerMCPClient,
    connections: dict[str, dict],
) -> dict[str, list[BaseTool]]:
    """Fetch every server's tools once, in parallel.

    Each ``get_tools`` call opens a fresh MCP session, so fetching once per
    server and filtering in memory (see ``select_tools``) avoids re-opening a
    session for the root agent and every subagent that shares a server. Total
    latency is bounded by the slowest server, not the sum.
    """

    async def _fetch(server_name: str) -> list[BaseTool]:
        try:
            tools = await client.get_tools(server_name=server_name)
            logger.info("Loaded %d tools from %s", len(tools), server_name)
            return tools
        except Exception as exc:
            logger.warning("Failed to load tools from %s: %s", server_name, type(exc).__name__)
            return []

    names = list(connections)
    per_server = await asyncio.gather(*(_fetch(n) for n in names))
    return dict(zip(names, per_server))


def select_tools(
    server_tools: dict[str, list[BaseTool]],
    connections: dict[str, dict],
    tool_entries: list[dict],
) -> list[BaseTool]:
    """Filter pre-fetched tools to those requested, by name AND server.

    Pure (no I/O): reads from the ``server_tools`` map produced by
    ``fetch_server_tools``. Prevents cross-server name collisions by only
    keeping tools whose name was requested on the same server that produced
    them.
    """
    url_to_name: dict[str, str] = {
        _normalize_url(conn.get("url")): name
        for name, conn in connections.items()
    }

    server_wanted: dict[str, set[str]] = {}
    for entry in tool_entries:
        url = _normalize_url(entry.get("mcp_server_url"))
        conn_name = url_to_name.get(url)
        # Builtin tools export a bare host URL (e.g. "https://tools.langchain.com")
        # while the connection URL is BUILTIN_MCP_URL (which includes the /mcp path),
        # so direct string matching misses. Route any builtin-matching entry to the
        # langsmith-tools connection when it exists.
        if conn_name is None and _is_builtin_server(url) and "langsmith-tools" in connections:
            conn_name = "langsmith-tools"
        if conn_name:
            server_wanted.setdefault(conn_name, set()).add(entry["name"])

    result: list[BaseTool] = []
    for server_name, wanted in server_wanted.items():
        tools = server_tools.get(server_name, [])
        result.extend(t for t in tools if t.name in wanted)
    return result


async def _connection_for(
    url: str, server: dict | None
) -> tuple[str, dict] | None:
    """Resolve a single URL into a (name, connection-spec) pair, or None to skip."""
    if _is_builtin_server(url):
        return "langsmith-tools", _builtin_connection(url)

    if server is None:
        logger.warning(
            "Skipping MCP server %s: not registered for this tenant in LangSmith",
            url,
        )
        return None

    auth_type = server.get("auth_type", "")
    name = _safe_server_name(url, server.get("name") or "server")

    if auth_type == "headers":
        headers = _headers_dict(server.get("headers"))
        if not headers:
            logger.warning(
                "Skipping MCP server %s: auth_type=headers but no headers returned "
                "(caller may lack mcp-servers:invoke permission)",
                url,
            )
            return None
        return name, _http_connection(url, headers)

    if auth_type == "oauth":
        provider_id = server.get("oauth_provider_id")
        # Per-user dynamic clients aren't registered for this user yet — the
        # registry returns null. Register on demand to get a provider_id.
        if not provider_id and server.get("oauth_mode") == "per_user_dynamic_client":
            provider_id = await _register_oauth_provider(server["id"])
        if not provider_id:
            logger.warning(
                "Skipping MCP server %s: no oauth_provider_id available "
                "(auth_type=oauth)",
                url,
            )
            return None
        token = await _get_oauth_token(provider_id)
        if not token:
            logger.warning(
                "Skipping MCP server %s: OAuth token fetch failed for provider %s",
                url, provider_id,
            )
            return None
        # The MCP server validates the token by calling back to LangSmith's
        # OAuth broker, which needs the user ID to resolve the grant.
        conn_headers = {"Authorization": f"Bearer {token}"}
        if user_id := _user_id():
            conn_headers["X-Ls-User-Id"] = user_id
        return name, _http_connection(url, conn_headers)

    logger.warning("Skipping MCP server %s: unknown auth_type %r", url, auth_type)
    return None


# --- LangSmith API ----------------------------------------------------------


async def _list_mcp_servers() -> list[dict]:
    """GET /v1/platform/fleet/mcp-servers — returns auth metadata per server.

    Each entry includes ``url``, ``auth_type``, ``oauth_provider_id`` (when
    ``auth_type == "oauth"``), ``oauth_mode``, and ``headers`` (when
    ``auth_type == "headers"`` and the caller has ``mcp-servers:invoke``).
    Fails soft.
    """
    if not os.environ.get("LANGSMITH_API_KEY", ""):
        logger.warning("LANGSMITH_API_KEY not set — cannot list MCP servers")
        return []

    url = f"{_langsmith_host()}/v1/platform/fleet/mcp-servers"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, headers=_langsmith_headers())
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as exc:
        logger.warning("Failed to list MCP servers from %s: HTTP %d", url, exc.response.status_code)
        return []
    except httpx.HTTPError as exc:
        logger.warning("Failed to list MCP servers from %s: %s", url, type(exc).__name__)
        return []


async def _register_oauth_provider(mcp_server_id: str) -> str | None:
    """POST /v1/platform/fleet/mcp-servers/{id}/oauth-provider.

    Registers this user against a per-user dynamic client MCP server,
    returning a stable ``oauth_provider_id`` that can then be exchanged
    for a token via ``/v2/auth/authenticate``. Idempotent.
    """
    user_id = _user_id()
    if not user_id:
        logger.warning(
            "Cannot register per-user OAuth provider for server %s: "
            "LANGSMITH_USER_ID not set.",
            mcp_server_id,
        )
        return None

    url = f"{_langsmith_host()}/v1/platform/fleet/mcp-servers/{mcp_server_id}/oauth-provider"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url, headers=_langsmith_headers(), json={"ls_user_id": user_id}
            )
            resp.raise_for_status()
            return resp.json().get("oauth_provider_id")
    except httpx.HTTPStatusError as exc:
        logger.warning(
            "Failed to register OAuth provider for %s: HTTP %d",
            mcp_server_id, exc.response.status_code,
        )
        return None
    except httpx.HTTPError as exc:
        logger.warning(
            "Failed to register OAuth provider for %s: %s",
            mcp_server_id, type(exc).__name__,
        )
        return None


async def _get_oauth_token(provider_id: str) -> str | None:
    """POST {host-backend}/v2/auth/authenticate — fetch an OAuth token.

    The OAuth broker lives on host-backend (``api.host.langchain.com``), not
    smith-backend. If a token is already provisioned for this (provider, user)
    pair, it is returned. Otherwise behavior depends on
    ``FLEET_OAUTH_INTERACTIVE``:

    - **non-interactive (default)**: makes a single request and, if the grant
      is still pending, logs how to authorize and returns None. Safe for
      headless deployments and LangGraph Studio — never opens a browser or
      blocks.
    - **interactive (opt-in)**: opens the consent URL in a browser and polls
      for completion for up to ``OAUTH_POLL_SECONDS``. Intended for a one-time
      local authorization from the CLI.

    Returns None on failure; the caller then skips the server (fail-soft, so
    one unprovisioned server never crashes agent startup).
    """
    api_key = os.environ.get("LANGSMITH_API_KEY", "")
    if not api_key:
        logger.warning("LANGSMITH_API_KEY not set — cannot fetch OAuth token")
        return None

    user_id = _user_id()
    if not user_id:
        logger.warning(
            "OAuth token fetch for %s requires LANGSMITH_USER_ID — set it in .env.",
            provider_id,
        )
        return None

    endpoint = f"{_host_backend_url()}/v2/auth/authenticate"
    body = {"provider": provider_id, "user_id": user_id, "scopes": []}
    headers = {"X-Api-Key": api_key}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if not _oauth_interactive():
                # Headless/default: one shot, no browser, no blocking.
                resp = await client.post(endpoint, headers=headers, json=body)
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") == "completed":
                    return data.get("token")
                logger.warning(
                    "OAuth token not provisioned for provider %s. Authorize once "
                    "locally with FLEET_OAUTH_INTERACTIVE=1 (e.g. via `make run`), "
                    "then redeploy.",
                    provider_id,
                )
                return None

            # Interactive: serialize so parallel resolution opens at most one
            # consent tab at a time.
            async with _OAUTH_BROWSER_LOCK:
                browser_opened = False
                for attempt in range(OAUTH_POLL_SECONDS + 1):
                    if attempt > 0:
                        await asyncio.sleep(1)
                    resp = await client.post(endpoint, headers=headers, json=body)
                    resp.raise_for_status()
                    data = resp.json()

                    if data.get("status") == "completed":
                        return data.get("token")
                    if data.get("status") != "pending" or not data.get("url"):
                        return None

                    if not browser_opened:
                        logger.info("Opening browser to authorize OAuth for %s", provider_id)
                        webbrowser.open(data["url"])
                        browser_opened = True

                logger.warning(
                    "OAuth authorization for %s timed out after %ds",
                    provider_id, OAUTH_POLL_SECONDS,
                )
    except httpx.HTTPStatusError as exc:
        logger.warning(
            "OAuth token fetch failed for %s: HTTP %d",
            provider_id, exc.response.status_code,
        )
    except httpx.HTTPError as exc:
        logger.warning(
            "OAuth token fetch failed for %s: %s", provider_id, type(exc).__name__
        )

    return None


def _langsmith_host() -> str:
    return os.environ.get("LANGSMITH_HOST_URL", DEFAULT_LANGSMITH_HOST).rstrip("/")


def _host_backend_url() -> str:
    """OAuth broker lives on host-backend, a separate service from smith-backend."""
    return os.environ.get("HOST_LANGCHAIN_API_URL", DEFAULT_HOST_BACKEND_URL).rstrip("/")


def _oauth_interactive() -> bool:
    """Whether to run the browser-based OAuth consent flow.

    Off by default so deployments and LangGraph Studio never open a browser or
    block on a 120s poll. Opt in with ``FLEET_OAUTH_INTERACTIVE=1`` for a
    one-time local authorization from the CLI.
    """
    return os.environ.get("FLEET_OAUTH_INTERACTIVE", "").strip().lower() in ("1", "true", "yes")


def _user_id() -> str:
    """LangSmith user UUID — required for OAuth token exchange and per-user grants.

    Read from ``LANGSMITH_USER_ID`` in the environment (typically loaded from
    ``.env``). Users find the value in ``fleet/config.json`` under
    ``metadata.ls_user_id``. Auto-resolving via ``/api/v1/me/ls_user_id``
    returns 403 for PAT auth, so callers should fail with a clear message
    rather than retry.
    """
    return os.environ.get("LANGSMITH_USER_ID", "")


def _langsmith_headers() -> dict[str, str]:
    """Common headers for LangSmith API calls.

    The ``/v1/platform/fleet/*`` routes require BOTH ``X-Tenant-Id`` and
    ``X-Organization-Id`` in prod — without them nginx 404s before hitting
    smith-go. Omit either and the handler is unreachable.

    Naming: in LangSmith's schema, "tenant" = workspace (not organization),
    so ``LANGSMITH_TENANT_ID`` is the workspace UUID and
    ``LANGSMITH_ORGANIZATION_ID`` is the containing org's UUID.
    """
    headers: dict[str, str] = {"X-Api-Key": os.environ.get("LANGSMITH_API_KEY", "")}
    if tenant_id := os.environ.get("LANGSMITH_TENANT_ID", ""):
        headers["X-Tenant-Id"] = tenant_id
    if org_id := os.environ.get("LANGSMITH_ORGANIZATION_ID", ""):
        headers["X-Organization-Id"] = org_id
    if user_id := _user_id():
        headers["X-Ls-User-Id"] = user_id
    return headers


# --- MCP connection helpers -------------------------------------------------


def _http_connection(url: str, headers: dict[str, str]) -> dict:
    return {
        "transport": "streamable_http",
        "url": url,
        "headers": headers,
        "timeout": timedelta(seconds=60),
    }


def _builtin_connection(raw_url: str) -> dict:
    """API-key-authed connection spec for the LangSmith builtin tool server.

    Tool invocation requires ``X-Ls-User-Id`` so LangSmith can look up the
    user's OAuth grants for services like Gmail/Calendar. Without it, tool
    calls fail with ``No ls_user_id available for OAuth``.
    """
    headers = _langsmith_headers()
    headers["X-Auth-Scheme"] = "langsmith-api-key"
    url = os.environ.get("BUILTIN_MCP_URL", raw_url)
    return _http_connection(url, headers)


def _is_builtin_server(url: str) -> bool:
    """Match by hostname against BUILTIN_MCP_URL — works for hosted, localhost, and self-hosted."""
    builtin = os.environ.get("BUILTIN_MCP_URL", "")
    return bool(builtin) and urlparse(builtin).hostname == urlparse(url).hostname


def _normalize_url(url: str | None) -> str:
    """Canonical form for URL-keyed lookups: trailing-slash stripped, lowercased."""
    return (url or "").rstrip("/").lower()


def _headers_dict(server_headers: list[dict] | None) -> dict[str, str]:
    """Convert LangSmith's ``[{key, value}, ...]`` header list to a dict."""
    if not server_headers:
        return {}
    return {
        h["key"]: h["value"]
        for h in server_headers
        if h.get("key") and h.get("value") is not None
    }


def _safe_server_name(url: str, server_name: str) -> str:
    """Derive a URL-safe connection name from the server name or hostname."""
    candidate = server_name.lower().replace(" ", "-")
    candidate = re.sub(r"[^a-z0-9-]", "", candidate).strip("-")
    if not candidate or candidate in ("server", "fleet"):
        host = urlparse(url).hostname or "server"
        candidate = host.split(".")[0].replace("-", "_")
    return candidate
