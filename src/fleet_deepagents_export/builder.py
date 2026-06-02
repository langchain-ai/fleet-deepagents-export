"""Load Fleet-exported agent config into components for create_deep_agent."""

from __future__ import annotations

import json
from pathlib import Path

from deepagents import SubAgent
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

from .parsers import parse_frontmatter
from .tools import build_connections, fetch_tools


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


async def _load_subagents(
    project_dir: Path,
    client: MultiServerMCPClient,
    connections: dict[str, dict],
) -> list[SubAgent]:
    """Load subagent definitions, fetching tools from the shared client."""
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
            sub_tools = await fetch_tools(client, connections, sub_entries)
            sub_interrupt = sub_config.get("interrupt_config", {})

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
    - ``interrupt_on``: dict from tools.json interrupt_config

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
    tools = await fetch_tools(client, connections, root_config.get("tools", []))
    subagents = await _load_subagents(project_dir, client, connections)

    return {
        "model": model,
        "system_prompt": system_prompt,
        "tools": tools,
        "subagents": subagents,
        "interrupt_on": root_config.get("interrupt_config"),
    }
