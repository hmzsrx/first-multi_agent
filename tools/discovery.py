from langchain.tools import tool


AGENT_REGISTRY = {
    "math_agent": {
        "description": "Handles mathematical questions and problem solving."
    },
    "python_agent": {
        "description": "Handles Python programming questions."
    },
    "english_agent": {
        "description": "Handles English grammar, vocabulary, and sentence correction."
    },
}


@tool
def list_agents(query: str = "") -> str:
    """Discover available study subagents. Optionally filter by a topic."""

    if not query:
        agents = AGENT_REGISTRY
    else:
        query = query.lower()

        agents = {
            name: info
            for name, info in AGENT_REGISTRY.items()
            if query in name.lower()
            or query in info["description"].lower()
        }

    if not agents:
        return "No matching agents found."

    return "\n".join(
        f"{name}: {info['description']}"
        for name, info in agents.items()
    )