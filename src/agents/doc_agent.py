import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from src.documents.tools import load_pdf_tool, clean_text_tool

load_dotenv()

TOOLS = [load_pdf_tool, clean_text_tool]

doc_agent = create_agent(
    model=os.getenv("CHAT_MODEL", "groq:openai/gpt-oss-120b"),
    tools=TOOLS,
    system_prompt=(
        "Tu es un assistant spécialisé dans l'analyse de documents. "
        "Tu utilises uniquement les tools fournis. "
        "Tu n'inventes jamais un résultat absent du document."
    ),
)

checkpointer = InMemorySaver()

chat_agent = create_agent(
    model=os.getenv("CHAT_MODEL", "groq:openai/gpt-oss-120b"),
    tools=[],
    system_prompt="Tu es un assistant utile et précis.",
    checkpointer=checkpointer,
)
