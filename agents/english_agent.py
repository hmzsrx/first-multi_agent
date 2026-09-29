from langchain.agents import create_agent
from langchain_groq import ChatGroq


model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


english_agent = create_agent(
    model=model,
    system_prompt="""
    You are an English specialist.
    Help with grammar, vocabulary, sentence correction,
    and English explanations.
    """
)