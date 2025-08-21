from src.core.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="Tu es un Assistant Intelligent de Documents."),
    HumanMessage(content="Explique Langchain en 1 phrase.")
]

response = llm.invoke(messages)
print(response.content)