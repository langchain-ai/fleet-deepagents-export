"""Standalone deepagent exported from LangSmith Fleet.

LangGraph Studio / dev server:  make dev
Terminal:                        make run  (see cli.py)

Extension points (edit these, not this file):
- ``custom_tools.py``      — add code-defined tools
- ``custom_middleware.py`` — wrap the agent loop with logging, filters, etc.
- ``custom_skills/``       — drop ``<skill-name>/SKILL.md`` files

Re-exports from Fleet overwrite ``fleet/`` but leave these files untouched.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from custom_middleware import custom_middleware
from custom_tools import custom_tools
from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from deepagents.middleware.skills import _parse_skill_metadata
from fleet_deepagent_export import load_agent_components
from langchain.agents.middleware.types import AgentMiddleware
from langgraph.runtime import Runtime

PROJECT_DIR = Path(__file__).parent
FLEET_DIR = PROJECT_DIR / "fleet"
CUSTOM_SKILLS_DIR = PROJECT_DIR / "custom_skills"

# Disk dirs -> virtual paths in agent state. Files at <disk>/foo/SKILL.md land
# at <virtual>/foo/SKILL.md so SkillsMiddleware can ls them.
_SKILL_SOURCES: dict[Path, str] = {
    FLEET_DIR / "skills": "/skills/fleet",
    CUSTOM_SKILLS_DIR: "/skills/custom",
}


def _load_skill_files() -> dict[str, dict]:
    """Read every SKILL.md (and supporting file) into a {vpath: FileData} dict.

    Skills must live in subdirectories (``<source>/<skill-name>/SKILL.md``);
    top-level files inside the source dir (``.gitkeep``, ``README.md``) are
    skipped — they can't form a valid skill and would just bloat state.
    """
    files: dict[str, dict] = {}
    for disk_dir, vroot in _SKILL_SOURCES.items():
        if not disk_dir.is_dir():
            continue
        for f in disk_dir.rglob("*"):
            if not f.is_file() or f.parent == disk_dir:
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rel = f.relative_to(disk_dir).as_posix()
            files[f"{vroot}/{rel}"] = create_file_data(content)
    return files


_STATIC_SKILL_FILES = _load_skill_files()


def _compute_skills_metadata() -> list[dict]:
    """Pre-parse SKILL.md frontmatter so we can inject skills_metadata directly.

    SkillsMiddleware runs before user middleware and caches `skills_metadata=[]`
    when it sees empty `state.files` on turn 1. Injecting both files and
    metadata in our before_agent lets our update overwrite that empty cache.
    """
    metadata: list[dict] = []
    for vpath, file_data in _STATIC_SKILL_FILES.items():
        if not vpath.endswith("/SKILL.md"):
            continue
        # /skills/fleet/<dir-name>/SKILL.md → dir_name is parts[-2]
        parts = vpath.rstrip("/").split("/")
        if len(parts) < 3:
            continue
        meta = _parse_skill_metadata(file_data["content"], vpath, parts[-2])
        if meta:
            metadata.append(meta)
    return metadata


_STATIC_SKILLS_METADATA = _compute_skills_metadata()


class StaticSkillsLoader(AgentMiddleware):
    """Inject static SKILL.md files and metadata into agent state on first turn.

    StateBackend is empty per-thread; without this, SkillsMiddleware finds no
    skills. We also inject ``skills_metadata`` directly so our update wins over
    SkillsMiddleware's empty-state cache. Caller-provided files via
    ``invoke(files=...)`` still merge in via the state reducer.
    """

    def before_agent(self, state: Any, runtime: Runtime) -> dict[str, Any] | None:
        update: dict[str, Any] = {}
        if not state.get("files"):
            update["files"] = _STATIC_SKILL_FILES
        if _STATIC_SKILLS_METADATA and not state.get("skills_metadata"):
            update["skills_metadata"] = _STATIC_SKILLS_METADATA
        return update or None


async def graph(runtime: Any):
    """Build and return the agent graph."""
    components = await load_agent_components(FLEET_DIR)
    model = components.pop("model")  # from fleet/config.json; replace to override
    components["tools"] = list(components["tools"]) + list(custom_tools)

    if _STATIC_SKILL_FILES:
        components["skills"] = [
            vroot for disk, vroot in _SKILL_SOURCES.items() if disk.is_dir()
        ]
        # backend left unset → defaults to StateBackend (in-state files)

    return create_deep_agent(
        model=model,
        middleware=[StaticSkillsLoader(), *custom_middleware],
        **components,
    ).with_config({"recursion_limit": 1000})
