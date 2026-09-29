from langchain.tools import tool

from agents.math_agent import math_agent
from agents.python_agent import python_agent
from agents.english_agent import english_agent


SUBAGENTS = {
    "math_agent": math_agent,
    "python_agent": python_agent,
    "english_agent": english_agent,
}


@tool
def task(agent_name: str, description: str) -> str:
    """Send a task to a specific study subagent."""

    agent = SUBAGENTS.get(agent_name)

    if agent is None:
        return f"Agent '{agent_name}' not found."

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"User's original question:\n{description}\n\n"
                    "Reply in the same language, writing script, and tone as "
                    "the original question. For example, use Roman Urdu for "
                    "Roman Urdu input and Urdu script for Urdu-script input. "
                    "Determine the response style from the original question, "
                    "not from these instructions."
                )
            }
        ]
    })

    return result["messages"][-1].content