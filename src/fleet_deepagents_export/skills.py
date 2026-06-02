"""Read SKILL.md from disk and inject into agent state on first turn.

Pre-parses ``skills_metadata`` to overwrite ``SkillsMiddleware``'s empty-state
cache (it runs first and caches ``[]`` from an empty ``state.files``).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deepagents.backends.utils import create_file_data
from deepagents.middleware.skills import _parse_skill_metadata
from langchain.agents.middleware.types import AgentMiddleware
from langgraph.runtime import Runtime


def _scan(
    sources: list[tuple[Path, str]],
) -> tuple[dict[str, dict], list[dict]]:
    """Walk sources (pre-filtered to existing dirs); skip top-level files."""
    files: dict[str, dict] = {}
    metadata: list[dict] = []
    for disk_dir, vroot in sources:
        for f in disk_dir.rglob("*"):
            if not f.is_file() or f.parent == disk_dir:
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rel = f.relative_to(disk_dir).as_posix()
            vpath = f"{vroot}/{rel}"
            files[vpath] = create_file_data(content)
            if f.name == "SKILL.md":
                meta = _parse_skill_metadata(content, vpath, f.parent.name)
                if meta:
                    metadata.append(meta)
    return files, metadata


class StaticSkillsLoader(AgentMiddleware):
    """Inject SKILL.md files into agent state on first turn.

    Pass instance to ``middleware=``; pass ``loader.skill_paths`` to ``skills=``.
    """

    def __init__(self, sources: list[tuple[Path, str]]) -> None:
        existing = [(d, v) for d, v in sources if d.is_dir()]
        self.files, self.metadata = _scan(existing)
        self.skill_paths = [v for _, v in existing]

    def before_agent(
        self, state: Any, runtime: Runtime
    ) -> dict[str, Any] | None:
        update: dict[str, Any] = {}
        # Per-key check so invoke(files={...}) doesn't suppress injection.
        state_files = state.get("files") or {}
        if not all(k in state_files for k in self.files):
            update["files"] = self.files
        if self.metadata and not state.get("skills_metadata"):
            update["skills_metadata"] = self.metadata
        return update or None
