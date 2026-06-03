"""Load Fleet-exported agent config into components for create_deep_agent."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from deepagents import SubAgent
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

from .parsers import parse_frontmatter
from .tools import build_connections, fetch_server_tools, select_tools

logger = logging.getLogger(__name__)


def _normalize_interrupt_config(
    interrupt_config: dict | None,
    valid_tool_names: set[str] | None = None,
) -> dict:
    """Map Fleet's composite interrupt keys to bare tool names.

    Fleet exports interrupt keys as ``"<server_url>::<tool_name>::<source>"``
    (e.g. ``"https://tools.langchain.com::gmail_send_email::Fleet"``), but
    ``HumanInTheLoopMiddleware`` matches interrupts by the bare tool-call name.
    Without this translation the approval gate never fires. Each key is reduced
    to its tool name — everything between the first (URL) and last (source)
    segments, so names containing ``"::"`` survive — and is idempotent when the
    key is already a bare name. Values (``True`` or an interrupt-config dict)
    pass through unchanged.

    ``interrupt_config`` controls agent execution flow, so when
    ``valid_tool_names`` is provided each normalized key is checked against it:
    entries that don't correspond to a loaded tool are dropped with a warning
    (they could never match a tool call anyway).
    """
    if not interrupt_config:
        return {}

    normalized: dict = {}
    for key, value in interrupt_config.items():
        parts = key.split("::")
        name = "::".join(parts[1:-1]) if len(parts) >= 3 else key
        if valid_tool_names is not None and name not in valid_tool_names:
            logger.warning(
                "Ignoring interrupt config for %r: no matching tool was loaded", name
            )
            continue
        if name in normalized and normalized[name] != value:
            logger.warning(
                "Conflicting interrupt config for tool %r; keeping the last entry", name
            )
        normalized[name] = value
    return normalized


def _load_all_tool_entries(project_dir: Path) -> tuple[dict, list[dict]]:
    """Read root tools.json and collect tool entries from all subagents.

    Returns (root_config, all_entries) where all_entries covers every server
    referenced by the agent and its subagents.
    """
    root_config = json.loads(
        (project_dir / "tools.json").read_text(encoding="utf-8")
    )
    entries: list[dict] = list(root_config.get("tools", []))

    subagents_dir = project_dir / "subagents"
    if subagents_dir.exists() and subagents_dir.is_dir():
        for subagent_dir in sorted(subagents_dir.iterdir()):
            tools_file = subagent_dir / "tools.json"
            if subagent_dir.is_dir() and tools_file.exists():
                sub_config = json.loads(tools_file.read_text(encoding="utf-8"))
                entries.extend(sub_config.get("tools", []))

    return root_config, entries


def _load_subagents(
    project_dir: Path,
    server_tools: dict[str, list],
    connections: dict[str, dict],
) -> list[SubAgent]:
    """Load subagent definitions, selecting tools from pre-fetched server tools.

    Pure in-memory filtering — no MCP I/O — so a server shared by the root
    agent and several subagents is fetched only once (see ``fetch_server_tools``).
    """
    subagents_dir = project_dir / "subagents"
    if not subagents_dir.exists() or not subagents_dir.is_dir():
        return []

    subagents: list[SubAgent] = []
    for subagent_dir in sorted(subagents_dir.iterdir()):
        if not subagent_dir.is_dir():
            continue

        agents_file = subagent_dir / "AGENTS.md"
        if not agents_file.exists():
            continue

        raw_md = agents_file.read_text(encoding="utf-8")
        meta, prompt = parse_frontmatter(raw_md)

        sub_tools = []
        sub_interrupt = {}
        tools_file = subagent_dir / "tools.json"
        if tools_file.exists():
            sub_config = json.loads(tools_file.read_text(encoding="utf-8"))
            sub_entries = sub_config.get("tools", [])
            sub_tools = select_tools(server_tools, connections, sub_entries)
            sub_interrupt = _normalize_interrupt_config(
                sub_config.get("interrupt_config"),
                {t.name for t in sub_tools},
            )

        subagents.append(
            SubAgent(
                name=subagent_dir.name,
                description=meta.get("description", ""),
                system_prompt=prompt,
                tools=sub_tools,
                interrupt_on=sub_interrupt,
            )
        )

    return subagents


def _load_model_id(project_dir: Path) -> str:
    """Read ``config.json`` and return ``config.configurable.llm_model_config.modelId``."""
    config_path = project_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path} not found. Drop your Fleet export into {project_dir}/ "
            f"(see {project_dir}/README.md)."
        )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    try:
        return config["config"]["configurable"]["llm_model_config"]["modelId"]
    except (KeyError, TypeError) as exc:
        raise ValueError(
            f"{config_path} is missing config.configurable.llm_model_config.modelId. "
            "Re-export from Fleet to regenerate it."
        ) from exc


async def load_agent_components(project_dir: Path) -> dict:
    """Read a Fleet export directory and return components for ``create_deep_agent()``.

    Returns a dict with:

    - ``model``: str from config.json (``llm_model_config.modelId``)
    - ``system_prompt``: str from AGENTS.md
    - ``tools``: list[BaseTool] from MCP servers
    - ``subagents``: list[SubAgent] from subagents/
    - ``interrupt_on``: dict from tools.json interrupt_config, keyed by tool name
      (Fleet's ``url::tool::source`` keys are normalized so the human-in-the-loop
      middleware matches them) — ``None`` when no tools require approval

    Skills and backend are *not* returned — the caller decides which
    directories to expose and how to scope filesystem access (e.g.
    ``FilesystemBackend(root_dir=...)`` or ``StateBackend``). See the
    starter's ``agent.py`` for the typical wiring.
    """
    load_dotenv(dotenv_path=project_dir / ".env")

    model = _load_model_id(project_dir)
    system_prompt = (project_dir / "AGENTS.md").read_text(encoding="utf-8")
    root_config, all_entries = _load_all_tool_entries(project_dir)

    connections = await build_connections(all_entries)
    client = MultiServerMCPClient(connections)
    # Fetch each server's tools once (parallel), then filter per consumer.
    server_tools = await fetch_server_tools(client, connections)
    tools = select_tools(server_tools, connections, root_config.get("tools", []))
    subagents = _load_subagents(project_dir, server_tools, connections)

    return {
        "model": model,
        "system_prompt": system_prompt,
        "tools": tools,
        "subagents": subagents,
        "interrupt_on": _normalize_interrupt_config(
            root_config.get("interrupt_config"),
            {t.name for t in tools},
        )
        or None,
    }
