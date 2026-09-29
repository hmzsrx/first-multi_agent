from langchain.agents import create_agent
from langchain_groq import ChatGroq


model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


math_agent = create_agent(
    model=model,
    system_prompt="""
    You are a Math specialist.
    Solve mathematical questions clearly and step by step.
    """
)