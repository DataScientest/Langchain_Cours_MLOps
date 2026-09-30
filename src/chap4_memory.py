import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

checkpointer = InMemorySaver()

agent = create_agent(
    model=os.getenv("CHAT_MODEL", "groq:openai/gpt-oss-120b"),
    tools=[],
    system_prompt="Tu es un assistant utile et précis.",
    checkpointer=checkpointer,
)

alice_config = {"configurable": {"thread_id": "alice"}}
bob_config = {"configurable": {"thread_id": "bob"}}
charlie_config = {"configurable": {"thread_id": "charlie"}}

agent.invoke(
    {"messages": [{"role": "user", "content": "Bonjour, je m'appelle Alice."}]},
    config=alice_config,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Bonjour, je m'appelle Bob."}]},
    config=bob_config,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Je suis étudiante en médecine."}]},
    config=alice_config,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Bonjour, je m'appelle Charlie."}]},
    config=charlie_config,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Je travaille dans la cybersécurité."}]},
    config=bob_config,
)

alice_result = agent.invoke(
    {"messages": [{"role": "user", "content": "Quel est mon nom et mon domaine d'étude ?"}]},
    config=alice_config,
)

bob_result = agent.invoke(
    {"messages": [{"role": "user", "content": "Quel est mon nom et mon domaine ?"}]},
    config=bob_config,
)

charlie_result = agent.invoke(
    {"messages": [{"role": "user", "content": "Quel est mon nom ?"}]},
    config=charlie_config,
)

print("Alice :", alice_result["messages"][-1].content)
print("Bob :", bob_result["messages"][-1].content)
print("Charlie :", charlie_result["messages"][-1].content)
