import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

checkpointer = InMemorySaver()

agent = create_agent(
    model=os.getenv("CHAT_MODEL", "groq:openai/gpt-oss-120b"),
    tools=[],
    system_prompt="Tu es un assistant pédagogique.",
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "alice"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Bonjour, je m'appelle Alice."}]},
    config=config,
)

print(response["messages"][-1].content)

agent.invoke(
    {"messages": [{"role": "user", "content": "J'étudie la médecine."}]},
    config=config,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Quel est mon domaine d'étude ?"}]},
    config=config,
)

print(result["messages"][-1].content)
