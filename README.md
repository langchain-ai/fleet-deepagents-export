# fleet-deepagents-export

Runtime support for agents exported from LangSmith Fleet. Reads the export config and wires up a deepagent with MCP tools, subagents, and skills.

Published on PyPI as [`fleet-deepagents-export`](https://pypi.org/project/fleet-deepagents-export/):

```bas
pip install fleet-deepagents-export
```

**This package is usually consumed via [`examples/template-agent/`](examples/template-agent) — a drop-in starter project that depends on it. Copy that directory, drop your Fleet export into `fleet/`, and run.**

## Quickstart

Requires [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.11+ (`uv` will fetch a compatible Python if you don't have one).

> Working with a coding agent (Claude Code, Cursor, etc.)? Point it at this repo and your `.zip` and ask it to set up the starter — the IDs it needs for `.env` are all in `fleet/config.json` after unzipping.

1. Grab the starter (it pulls `fleet-deepagents-export` from PyPI as a normal dependency):
   ```bash
   git clone --depth 1 https://github.com/langchain-ai/fleet-deepagents-export.git
   cp -R fleet-deepagents-export/examples/template-agent my-agent && cd my-agent
   ```
   Or, if you'd rather wire things up by hand, `pip install fleet-deepagents-export` into your own project and follow the layout described under [What the package reads](#what-the-package-reads).
2. Export your agent from LangSmith Fleet (the `.zip`), then drop the contents into `fleet/` (which ships empty apart from a placeholder README):
   ```bash
   unzip path/to/my-export.zip -d fleet/
   ```
3. Fill in `.env`:
   ```bash
   cp .env.example .env   # then edit
   ```
   The three `LANGSMITH_*_ID` values live in `fleet/config.json` under `metadata` — just copy them across.
4. Run:
   ```bash
   make setup    # install dependencies (uv sync)

   # then use one of these to interact with the agent:
   make dev      # LangGraph Studio — browser UI for chatting with the agent and inspecting graph state
   make run      # terminal REPL via cli.py — text-only chat
   ```

Re-exporting from Fleet later? Wipe and re-unzip — the rest of your project is untouched:
```bash
rm -rf fleet && unzip path/to/my-new-export.zip -d fleet/
```

## What's editable in the starter

The starter separates "code from Fleet" from "code you add":

- `fleet/` — owned by Fleet. Ships empty (just a placeholder README); drop your export contents here (`AGENTS.md`, `config.json`, `tools.json`, optional `subagents/` and `skills/`). Re-unzip a fresh export to update; nothing else is touched.
- `agent.py` — graph wiring. The model comes from `fleet/config.json`; replace the `model = components.pop("model")` line to override. The starter ships with `langchain-anthropic`, `langchain-openai`, and `langchain-google-genai` installed — for any other provider prefix (`bedrock:`, `mistralai:`, etc.), add the matching `langchain-<provider>` package to `pyproject.toml`.
- `custom_tools.py` — owned by you. Add code-defined tools; merged with Fleet MCP tools at runtime.
- `custom_middleware.py` — owned by you. Add `AgentMiddleware` instances for logging, filters, pre/post hooks, etc.
- `custom_skills/` — owned by you. Drop `<skill-name>/SKILL.md` files here; layered on top of `fleet/skills/` (later overrides earlier when names collide). Files are read at module load and injected into agent state — the agent never reads disk at request time.
- `cli.py` — terminal REPL; edit freely for a different I/O loop.
- `pyproject.toml` — rename the project, pin deps.

## What the package reads

From the `fleet/` directory:

- `AGENTS.md` → system prompt
- `tools.json` → MCP server connections (builtin / OAuth / bearer token)
- `subagents/<name>/AGENTS.md` + `tools.json` → subagent definitions
- `skills/*/SKILL.md` → skill instructions

## MCP auth

At startup, each tool's `mcp_server_url` is resolved against LangSmith's
MCP server registry. One round-trip, then connections are built per the
registry's auth info. Three paths:

- **Builtin LangSmith tools** (Gmail, Calendar, builtin GitHub) — authed
  via your PAT.
- **Static-credential servers** (`auth_type: "headers"`) — credentials
  come from the registry record. Requires `mcp-servers:invoke` permission.
- **OAuth servers** (`auth_type: "oauth"`) — bearer token fetched from
  LangSmith's OAuth broker. A browser opens on first run for any per-user
  server that isn't yet authorized for your user.

Servers not in the registry are skipped with a warning.

## Env vars

| Name | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | yes (default) | Model provider. `create_deep_agent` accepts any LangChain-compatible prefix (`anthropic:`, `openai:`, `google-genai:`, etc.) — set the matching provider's API key instead if you override the model in `agent.py`. |
| `LANGSMITH_API_KEY` | yes | PAT with `mcp-servers:read` + `mcp-servers:invoke`. Used by this library for MCP registry lookup and builtin-server auth. |
| `LANGSMITH_TENANT_ID` | yes | Workspace UUID. Copy from `fleet/config.json` → `metadata.tenant_id`. Required so the LangSmith API can route `/v1/platform/fleet/*` requests to your workspace; without it, requests fail with a 404 before reaching the handler. |
| `LANGSMITH_ORGANIZATION_ID` | yes | Org UUID. Copy from `fleet/config.json` → `metadata.organization_id`. Required alongside `LANGSMITH_TENANT_ID`. |
| `LANGSMITH_USER_ID` | yes (if any OAuth tool) | User UUID. Copy from `fleet/config.json` → `metadata.ls_user_id`. Used for OAuth token exchange and builtin-server per-user grant lookup. |
| `BUILTIN_MCP_URL` | yes (if any builtin tool) | e.g. `https://tools.langchain.com/mcp`. Hostname is used to detect which tool entries route to the builtin server. Hosted, localhost, and self-hosted deployments each set it to their respective URL. |
| `LANGSMITH_HOST_URL` | yes (if self-hosted) | LangSmith API host. Cloud users can leave unset (defaults to `https://api.smith.langchain.com`). For self-hosted, set to your LangSmith hostname with `/api` appended. Example: if your LangSmith is at `https://langsmith.acme.com`, set this to `https://langsmith.acme.com/api`. |
| `HOST_LANGCHAIN_API_URL` | yes (if self-hosted with OAuth tools) | OAuth broker host. Cloud users can leave unset (defaults to `https://api.host.langchain.com`). For self-hosted with OAuth-backed Fleet tools (Gmail, GitHub, etc.), set to your LangSmith hostname with `/api-host` appended. Example: `https://langsmith.acme.com/api-host`. Your self-hosted deployment must have Fleet enabled (`config.deployment.enabled: true` in helm values) — see the [self-hosted Fleet setup docs](https://docs.langchain.com/langsmith/deploy-self-hosted-full-platform). |

