"""Terminal entry point for the agent.

Run with:
    make run

Builds the agent via ``agent.graph`` and drives it interactively.
``agent.py`` itself stays focused on graph construction — anything
about user input/output lives here.
"""

from __future__ import annotations

import asyncio

from agent import graph


async def main() -> None:
    agent = await graph({})
    print("Agent ready. Type a message (Ctrl+C to quit).\n")
    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            return

        if not user_input.strip():
            continue

        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        print(f"Agent: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    asyncio.run(main())
