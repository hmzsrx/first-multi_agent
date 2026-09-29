from dotenv import load_dotenv

# FIRST: load .env
load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.discovery import list_agents
from tools.task import task
import os




GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to the project's .env file or set it in your environment."
    )


model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)



main_agent = create_agent(
    model=model,
    tools=[list_agents, task],
    system_prompt="""
    You are a Study Assistant.

    Always reply in the same language, writing script, and tone as the user's
    message. For example, reply in Roman Urdu to Roman Urdu and in Urdu script
    to Urdu-script input. For mixed-language messages, follow the dominant
    language and preserve commonly used technical terms.

    You have access to specialized study subagents.

    For every user message, first decide whether one of these specialists
    matches the question:

    - Python programming, code, or Python errors: python_agent
    - Mathematics, calculations, or solving equations: math_agent
    - English grammar, vocabulary, sentence correction, or English learning: english_agent

    If a specialist matches, you MUST use list_agents to discover it, then
    call task with that agent_name and the user's original question. Do not
    answer that question yourself. Return the specialist's answer without
    adding to or rewriting it.

    If the question does not match any available specialist, answer it
    yourself. If it clearly needs more than one specialist, call each relevant
    specialist and combine their answers without inventing information.
    """
)


while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    called_agents = [
    ]
    print("\nAssistant: ", end="", flush=True)

    for mode, chunk in main_agent.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode=["messages", "updates"],
    ):
        if mode == "messages":
            message, metadata = chunk
            if metadata.get("langgraph_node") != "model":
                continue
            if getattr(message, "tool_call_chunks", None):
                continue
            if isinstance(message.content, str):
                print(message.content, end="", flush=True)
            elif isinstance(message.content, list):
                for block in message.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        print(block.get("text", ""), end="", flush=True)
        elif mode == "updates":
            for node_update in chunk.values():
                for message in node_update.get("messages", []):
                    for tool_call in getattr(message, "tool_calls", []):
                        if tool_call.get("name") == "task":
                            agent_name = tool_call.get("args", {}).get("agent_name")
                            if agent_name and agent_name not in called_agents:
                                called_agents.append(agent_name)

    print()

    if called_agents:
        print("Agent called:", ", ".join(called_agents))
    else:
        print("Agent called: none")