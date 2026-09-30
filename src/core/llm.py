import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

def get_llm():
    model_name = os.getenv("CHAT_MODEL", "groq:openai/gpt-oss-120b")
    return init_chat_model(model_name)

llm = get_llm()
