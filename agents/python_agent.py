from langchain.agents import create_agent
from langchain_groq import ChatGroq


model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


python_agent = create_agent(
    model=model,
    system_prompt="""
    You are a Python specialist.
    Explain Python concepts simply with examples.
    """
)