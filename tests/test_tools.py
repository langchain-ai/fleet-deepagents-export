"""Minimal tests for fleet_deepagents_export.tools.

Covers pure helpers and the public entry points (build_connections,
fetch_server_tools, select_tools) with the registry call and MCP client
stubbed out. The OAuth flow is covered for its interactive/non-interactive
branching with httpx stubbed out.
"""

from __future__ import annotations

import pytest

from fleet_deepagents_export import tools as mod


# --- Pure helpers -----------------------------------------------------------


@pytest.mark.parametrize(
    "given,expected",
    [
        (None, ""),
        ("", ""),
        ("https://example.com", "https://example.com"),
        ("https://example.com/", "https://example.com"),
        ("https://EXAMPLE.com/mcp/", "https://example.com/mcp"),
    ],
)
def test_normalize_url(given, expected):
    assert mod._normalize_url(given) == expected


def test_safe_server_name_sanitizes_display_name():
    assert mod._safe_server_name("https://x.example.com", "My Slack!") == "my-slack"


def test_safe_server_name_falls_back_to_host_when_generic():
    # Generic names ("server", "fleet") are replaced with the URL host.
    assert mod._safe_server_name("https://tools.langchain.com/mcp", "server") == "tools"
    assert mod._safe_server_name("https://foo-bar.example.com", "fleet") == "foo_bar"


def test_headers_dict_converts_list_of_pairs():
    out = mod._headers_dict(
        [{"key": "A", "value": "1"}, {"key": "B", "value": "2"}]
    )
    assert out == {"A": "1", "B": "2"}


def test_headers_dict_skips_missing_or_none():
    out = mod._headers_dict(
        [
            {"key": "A", "value": "1"},
            {"key": "", "value": "2"},
            {"key": "C", "value": None},
        ]
    )
    assert out == {"A": "1"}


def test_headers_dict_handles_none():
    assert mod._headers_dict(None) == {}


def test_is_builtin_server_matches_by_hostname(monkeypatch):
    monkeypatch.setenv("BUILTIN_MCP_URL", "https://tools.langchain.com/mcp")
    assert mod._is_builtin_server("https://tools.langchain.com")
    assert mod._is_builtin_server("https://tools.langchain.com/anything")
    assert not mod._is_builtin_server("https://other.example.com/mcp")


def test_is_builtin_server_false_without_env(monkeypatch):
    monkeypatch.delenv("BUILTIN_MCP_URL", raising=False)
    assert not mod._is_builtin_server("https://tools.langchain.com")


# --- build_connections ------------------------------------------------------


@pytest.fixture
def clean_env(monkeypatch):
    """Clear LangSmith-related env vars so each test starts from a known state."""
    for key in (
        "LANGSMITH_API_KEY",
        "LANGSMITH_TENANT_ID",
        "LANGSMITH_ORGANIZATION_ID",
        "LANGSMITH_USER_ID",
        "BUILTIN_MCP_URL",
        "LANGSMITH_HOST_URL",
        "HOST_LANGCHAIN_API_URL",
        "FLEET_OAUTH_INTERACTIVE",
    ):
        monkeypatch.delenv(key, raising=False)
    return monkeypatch


async def test_build_connections_empty():
    assert await mod.build_connections([]) == {}


async def test_build_connections_builtin_only_skips_registry(clean_env):
    clean_env.setenv("BUILTIN_MCP_URL", "https://tools.langchain.com/mcp")
    clean_env.setenv("LANGSMITH_API_KEY", "k")

    async def _must_not_call():
        raise AssertionError("registry should not be fetched when every URL is builtin")

    clean_env.setattr(mod, "_list_mcp_servers", _must_not_call)

    entries = [{"name": "gmail.send", "mcp_server_url": "https://tools.langchain.com"}]
    conns = await mod.build_connections(entries)

    assert list(conns) == ["langsmith-tools"]
    spec = conns["langsmith-tools"]
    assert spec["url"] == "https://tools.langchain.com/mcp"
    assert spec["headers"]["X-Api-Key"] == "k"
    assert spec["headers"]["X-Auth-Scheme"] == "langsmith-api-key"


async def test_build_connections_dedupes_case_insensitively(clean_env):
    clean_env.setenv("BUILTIN_MCP_URL", "https://tools.langchain.com/mcp")
    clean_env.setenv("LANGSMITH_API_KEY", "k")

    entries = [
        {"name": "a", "mcp_server_url": "https://tools.langchain.com"},
        {"name": "b", "mcp_server_url": "https://TOOLS.langchain.com/"},
    ]
    conns = await mod.build_connections(entries)
    assert list(conns) == ["langsmith-tools"]


async def test_build_connections_resolves_headers_auth(clean_env):
    clean_env.setenv("LANGSMITH_API_KEY", "k")

    async def _registry():
        return [
            {
                "url": "https://slack.example.com",
                "name": "Slack",
                "auth_type": "headers",
                "headers": [{"key": "X-Slack-Token", "value": "t"}],
            }
        ]

    clean_env.setattr(mod, "_list_mcp_servers", _registry)

    entries = [{"name": "send", "mcp_server_url": "https://slack.example.com"}]
    conns = await mod.build_connections(entries)

    assert list(conns) == ["slack"]
    assert conns["slack"]["url"] == "https://slack.example.com"
    assert conns["slack"]["headers"] == {"X-Slack-Token": "t"}


async def test_build_connections_skips_unregistered(clean_env):
    clean_env.setenv("LANGSMITH_API_KEY", "k")

    async def _empty():
        return []

    clean_env.setattr(mod, "_list_mcp_servers", _empty)

    entries = [{"name": "x", "mcp_server_url": "https://ghost.example.com"}]
    assert await mod.build_connections(entries) == {}


async def test_build_connections_disambiguates_name_collisions(clean_env):
    clean_env.setenv("LANGSMITH_API_KEY", "k")

    async def _registry():
        return [
            {
                "url": "https://slack.a.com",
                "name": "Slack",
                "auth_type": "headers",
                "headers": [{"key": "H", "value": "v1"}],
            },
            {
                "url": "https://slack.b.com",
                "name": "Slack",
                "auth_type": "headers",
                "headers": [{"key": "H", "value": "v2"}],
            },
        ]

    clean_env.setattr(mod, "_list_mcp_servers", _registry)

    entries = [
        {"name": "t1", "mcp_server_url": "https://slack.a.com"},
        {"name": "t2", "mcp_server_url": "https://slack.b.com"},
    ]
    conns = await mod.build_connections(entries)

    assert sorted(conns) == ["slack", "slack-2"]
    urls = {conns[n]["url"] for n in conns}
    assert urls == {"https://slack.a.com", "https://slack.b.com"}


# --- fetch_server_tools / select_tools --------------------------------------


class _FakeTool:
    def __init__(self, name: str):
        self.name = name


class _FakeClient:
    """Stub of MultiServerMCPClient — only implements get_tools(server_name=...)."""

    def __init__(self, by_server: dict[str, list[_FakeTool]]):
        self._by_server = by_server
        self.calls: list[str] = []

    async def get_tools(self, server_name: str):
        self.calls.append(server_name)
        return list(self._by_server.get(server_name, []))


async def test_fetch_server_tools_fetches_each_server_once():
    client = _FakeClient(
        {
            "server_a": [_FakeTool("a1")],
            "server_b": [_FakeTool("b1")],
        }
    )
    connections = {
        "server_a": {"url": "https://a.example.com"},
        "server_b": {"url": "https://b.example.com"},
    }

    server_tools = await mod.fetch_server_tools(client, connections)

    # Each server is fetched exactly once (no per-consumer re-fetch).
    assert sorted(client.calls) == ["server_a", "server_b"]
    assert [t.name for t in server_tools["server_a"]] == ["a1"]
    assert [t.name for t in server_tools["server_b"]] == ["b1"]


def test_select_tools_filters_by_name():
    server_tools = {"server_a": [_FakeTool("send"), _FakeTool("extra")]}
    connections = {"server_a": {"url": "https://a.example.com"}}
    entries = [{"name": "send", "mcp_server_url": "https://a.example.com"}]

    tools = mod.select_tools(server_tools, connections, entries)
    assert [t.name for t in tools] == ["send"]


def test_select_tools_does_not_leak_same_name_across_servers():
    # Both servers expose "ping" but only server_a was asked for it.
    server_tools = {
        "server_a": [_FakeTool("ping")],
        "server_b": [_FakeTool("ping")],
    }
    connections = {
        "server_a": {"url": "https://a.example.com"},
        "server_b": {"url": "https://b.example.com"},
    }
    entries = [{"name": "ping", "mcp_server_url": "https://a.example.com"}]

    tools = mod.select_tools(server_tools, connections, entries)
    assert len(tools) == 1


def test_select_tools_routes_builtin_host_url(monkeypatch):
    # Builtin entries list the bare host; the connection URL includes /mcp.
    # select_tools must bridge the gap via _is_builtin_server().
    monkeypatch.setenv("BUILTIN_MCP_URL", "https://tools.langchain.com/mcp")
    server_tools = {
        "langsmith-tools": [_FakeTool("gmail.send"), _FakeTool("gmail.search")]
    }
    connections = {"langsmith-tools": {"url": "https://tools.langchain.com/mcp"}}
    entries = [{"name": "gmail.send", "mcp_server_url": "https://tools.langchain.com"}]

    tools = mod.select_tools(server_tools, connections, entries)
    assert [t.name for t in tools] == ["gmail.send"]


# --- _get_oauth_token (interactive vs headless) -----------------------------


class _FakeResp:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _FakeHTTPClient:
    """Async-context stub for httpx.AsyncClient returning queued payloads."""

    def __init__(self, payloads: list[dict]):
        self._payloads = list(payloads)
        self.post_calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def post(self, *args, **kwargs):
        self.post_calls += 1
        idx = min(self.post_calls - 1, len(self._payloads) - 1)
        return _FakeResp(self._payloads[idx])


def _patch_httpx(monkeypatch, payloads: list[dict]):
    monkeypatch.setattr(mod.httpx, "AsyncClient", lambda *a, **k: _FakeHTTPClient(payloads))


async def test_get_oauth_token_non_interactive_skips_browser(clean_env):
    clean_env.setenv("LANGSMITH_API_KEY", "k")
    clean_env.setenv("LANGSMITH_USER_ID", "u")
    _patch_httpx(clean_env, [{"status": "pending", "url": "https://consent"}])

    opened: list[str] = []
    clean_env.setattr(mod.webbrowser, "open", lambda url: opened.append(url))

    async def _no_sleep(*a, **k):
        raise AssertionError("non-interactive OAuth must not sleep/poll")

    clean_env.setattr(mod.asyncio, "sleep", _no_sleep)

    token = await mod._get_oauth_token("prov")
    assert token is None
    assert opened == []  # no browser in headless/default mode


async def test_get_oauth_token_returns_already_provisioned_token(clean_env):
    clean_env.setenv("LANGSMITH_API_KEY", "k")
    clean_env.setenv("LANGSMITH_USER_ID", "u")
    _patch_httpx(clean_env, [{"status": "completed", "token": "T"}])

    assert await mod._get_oauth_token("prov") == "T"


async def test_get_oauth_token_interactive_opens_browser_then_polls(clean_env):
    clean_env.setenv("LANGSMITH_API_KEY", "k")
    clean_env.setenv("LANGSMITH_USER_ID", "u")
    clean_env.setenv("FLEET_OAUTH_INTERACTIVE", "1")
    _patch_httpx(
        clean_env,
        [
            {"status": "pending", "url": "https://consent"},
            {"status": "completed", "token": "T"},
        ],
    )

    opened: list[str] = []
    clean_env.setattr(mod.webbrowser, "open", lambda url: opened.append(url))

    async def _fast_sleep(*a, **k):
        return None

    clean_env.setattr(mod.asyncio, "sleep", _fast_sleep)

    token = await mod._get_oauth_token("prov")
    assert token == "T"
    assert opened == ["https://consent"]  # browser flow runs only when opted in

