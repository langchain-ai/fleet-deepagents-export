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

import asyncio
import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from custom_middleware import custom_middleware
from custom_tools import custom_tools
from deepagents import create_deep_agent
from fleet_deepagents_export import StaticSkillsLoader, load_agent_components

PROJECT_DIR = Path(__file__).parent
FLEET_DIR = PROJECT_DIR / "fleet"
CUSTOM_SKILLS_DIR = PROJECT_DIR / "custom_skills"

# Read SKILL.md from disk once; middleware injects into state on first turn.
_SKILL_LOADER = StaticSkillsLoader(
    [
        (FLEET_DIR / "skills", "/skills/fleet"),
        (CUSTOM_SKILLS_DIR, "/skills/custom"),
    ]
)

# LangGraph re-invokes this module's ``graph`` factory on *every* run (Studio
# message, deployment request), so without caching every run would re-resolve
# MCP connections and re-fetch tools. Build the components once per process and
# reuse them for FLEET_COMPONENTS_TTL seconds. OAuth tokens are baked into
# connection headers at build time, so the TTL bounds how stale they can get;
# set it to 0 to disable caching and rebuild every run.
_COMPONENTS_CACHE: dict | None = None
_COMPONENTS_AT: float = 0.0
_COMPONENTS_LOCK = asyncio.Lock()


def _cache_ttl() -> float:
    try:
        return float(os.environ.get("FLEET_COMPONENTS_TTL", "600"))
    except ValueError:
        return 600.0


async def _get_components() -> dict:
    """Return cached agent components, rebuilding when the TTL has elapsed.

    Double-checked locking: the fast path avoids the lock on cache hits; under
    concurrent runs only one coroutine rebuilds. The cache is updated only on a
    successful build, so a failed load leaves the previous components intact and
    propagates the error rather than caching a partial result.
    """
    global _COMPONENTS_CACHE, _COMPONENTS_AT
    ttl = _cache_ttl()
    if _COMPONENTS_CACHE is not None and (time.monotonic() - _COMPONENTS_AT) < ttl:
        return _COMPONENTS_CACHE

    async with _COMPONENTS_LOCK:
        if _COMPONENTS_CACHE is not None and (time.monotonic() - _COMPONENTS_AT) < ttl:
            return _COMPONENTS_CACHE
        components = await load_agent_components(FLEET_DIR)
        _COMPONENTS_CACHE = components
        _COMPONENTS_AT = time.monotonic()
        return _COMPONENTS_CACHE


async def graph(runtime: Any):
    """Build and return the agent graph."""
    # Shallow-copy the cached dict: graph() mutates it (pops "model", rebuilds
    # "tools"), and the cache must stay pristine for the next run.
    components = dict(await _get_components())
    model = components.pop("model")  # from fleet/config.json; replace to override
    components["tools"] = list(components["tools"]) + list(custom_tools)

    if _SKILL_LOADER.files:
        components["skills"] = _SKILL_LOADER.skill_paths

    return create_deep_agent(
        model=model,
        middleware=[_SKILL_LOADER, *custom_middleware],
        **components,
    ).with_config({"recursion_limit": 1000})
