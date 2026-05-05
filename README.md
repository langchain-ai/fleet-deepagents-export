# fleet-deepagent-export

Runtime support for agents exported from LangSmith Fleet. Reads the export config and wires up a deepagent with MCP tools, subagents, and skills.

**This package is usually consumed via [`examples/template-agent/`](examples/template-agent) — a drop-in starter project that imports it. Copy that directory, drop your Fleet export into `fleet/`, and run.**

## Quickstart

1. Copy the starter out of this repo and rename it:
   ```bash
   cp -R examples/template-agent my-agent && cd my-agent
   ```
2. Export your agent from LangSmith Fleet (the `.zip`), then drop the contents into `fleet/`:
   ```bash
   unzip ~/Downloads/my-export.zip -d fleet/
   ```
3. Fill in `.env`:
   ```bash
   cp .env.example .env   # then edit
   ```
4. Run:
   ```bash
   make setup    # uv sync
   make dev      # LangGraph dev server — opens Studio
   make run      # terminal REPL
   ```

Re-exporting from Fleet later? Wipe and re-unzip — the rest of your project is untouched:
```bash
rm -rf fleet && unzip ~/Downloads/my-new-export.zip -d fleet/
```

## What's editable in the starter

The starter separates "code from Fleet" from "code you add":

- `fleet/` (AGENTS.md, tools.json, subagents/, skills/) — owned by Fleet. Re-unzip a fresh export here to update; nothing else is touched.
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
| `LANGSMITH_API_KEY` | yes | PAT with `mcp-servers:read` + `mcp-servers:invoke`. Used for tracing, registry lookup, and builtin-server auth. |
| `LANGSMITH_TENANT_ID` | yes | Workspace UUID. Required for `/v1/platform/fleet/*` routing in prod; without it, nginx 404s before hitting smith-go. |
| `LANGSMITH_ORGANIZATION_ID` | yes | Same — required alongside `LANGSMITH_TENANT_ID`. |
| `LANGSMITH_USER_ID` | yes (if any OAuth tool) | User UUID for OAuth token exchange and builtin-server per-user grant lookup. Auto-resolution via `/me` 403s for PATs, so set explicitly. |
| `BUILTIN_MCP_URL` | yes (if any builtin tool) | e.g. `https://tools.langchain.com/mcp`. Hostname is used to detect which tool entries route to the builtin server. Hosted, localhost, and self-hosted deployments each set it to their respective URL. |
| `LANGSMITH_HOST_URL` | no | Override smith-backend host (default `https://api.smith.langchain.com`). Needed for self-hosted. |
| `HOST_LANGCHAIN_API_URL` | no | Override the OAuth broker host (default `https://api.host.langchain.com`). Needed for self-hosted. |

## Install

The starter's `pyproject.toml` already depends on this package via a git
URL pointing at this repo, so `make setup` pulls it in — you typically
don't install it by hand.

If you want it in your own project directly (no starter), add to your
dependencies:

```
fleet-deepagent-export @ git+https://github.com/langchain-ai/tmp-fleet-download-code.git
```

(Will be published to PyPI once the API stabilizes.)
