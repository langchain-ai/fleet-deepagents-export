"""Code-defined tools to add on top of the Fleet export.

Tools declared here are merged with the MCP tools from ``tools.json`` at
runtime. Edit this file to extend the agent; ``agent.py`` and ``tools.json``
stay untouched so future re-exports from Fleet won't conflict with your
custom code.

See https://python.langchain.com/docs/concepts/tools/ for the ``@tool`` API.
"""

from __future__ import annotations

from langchain_core.tools import BaseTool, tool  # noqa: F401 — `tool` is re-exported for scaffolded tools below

# Example — define a tool AND include it in ``custom_tools`` below.
# ``agent.py`` imports this list and passes it to ``create_deep_agent``;
# a @tool-decorated function that isn't in the list never reaches the agent.
#
# @tool
# def double(x: int) -> int:
#     """Return twice the input."""
#     return x * 2

custom_tools: list[BaseTool] = []  # e.g. [double]
