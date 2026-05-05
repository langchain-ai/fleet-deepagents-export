"""Middleware to add on top of the Fleet export.

Middleware listed here is passed to ``create_deep_agent(middleware=...)``.
Use it for logging, rate limiting, content filtering, custom routing,
pre/post-processing of messages, or any behavior that wraps the agent
loop rather than adding tools to it.

See langchain-docs for the ``AgentMiddleware`` interface and examples.
"""

from __future__ import annotations

from langchain.agents.middleware import AgentMiddleware

# Example — define a middleware class AND include an instance in
# ``custom_middleware`` below. ``agent.py`` imports this list and passes it
# to ``create_deep_agent``; a class that isn't instantiated into the list
# never runs.
#
# class LoggingMiddleware(AgentMiddleware):
#     async def before_model(self, state, runtime):
#         print(f"[middleware] sending {len(state['messages'])} messages to model")

custom_middleware: list[AgentMiddleware] = []  # e.g. [LoggingMiddleware()]
