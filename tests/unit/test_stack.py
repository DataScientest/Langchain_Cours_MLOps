"""Shared tests for every branch: the LangChain 1.x stack works without an API key."""

import importlib

import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field

from src.core.tools import char_count, word_count
from tests.fakes import ToolCallingFakeChatModel


@pytest.mark.parametrize(
    "module",
    [
        "langchain",
        "langchain.agents",
        "langchain.chat_models",
        "langchain.tools",
        "langchain_core",
        "langchain_groq",
        "langchain_openai",
        "langgraph.checkpoint.memory",
        "langsmith",
        "src.core.llm",
        "src.core.tools",
    ],
)
def test_imports(module):
    importlib.import_module(module)


class Category(BaseModel):
    category: str
    confidence: float = Field(ge=0, le=1)


def test_prompt_fake_model_structured_output():
    model = ToolCallingFakeChatModel(
        messages=iter([
            AIMessage(
                content="",
                tool_calls=[{"name": "Category", "args": {"category": "IA", "confidence": 0.9}, "id": "c1"}],
            )
        ])
    )
    prompt = ChatPromptTemplate.from_messages([("human", "Texte : {input}")])
    chain = prompt | model.with_structured_output(Category)

    result = chain.invoke({"input": "Les réseaux de neurones apprennent."})

    assert result == Category(category="IA", confidence=0.9)


def test_create_agent_calls_tool():
    model = ToolCallingFakeChatModel(
        messages=iter([
            AIMessage(
                content="",
                tool_calls=[{"name": "word_count", "args": {"text": "un deux trois"}, "id": "t1"}],
            ),
            AIMessage(content="Le texte contient 3 mots."),
        ])
    )
    agent = create_agent(model, tools=[word_count, char_count], system_prompt="Tu comptes les mots.")

    result = agent.invoke({"messages": [{"role": "user", "content": "Compte les mots de 'un deux trois'."}]})

    tool_messages = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    assert len(tool_messages) == 1
    assert tool_messages[0].name == "word_count"
    assert tool_messages[0].content == "3"
    assert result["messages"][-1].content == "Le texte contient 3 mots."


def test_memory_keeps_context_on_same_thread_id():
    model = ToolCallingFakeChatModel(
        messages=iter([AIMessage(content="Bonjour Alice."), AIMessage(content="Vous vous appelez Alice.")])
    )
    agent = create_agent(model, tools=[], checkpointer=InMemorySaver())
    alice = {"configurable": {"thread_id": "alice"}}

    agent.invoke({"messages": [{"role": "user", "content": "Je m'appelle Alice."}]}, config=alice)
    result = agent.invoke({"messages": [{"role": "user", "content": "Comment je m'appelle ?"}]}, config=alice)

    contents = [m.content for m in result["messages"]]
    assert contents == [
        "Je m'appelle Alice.",
        "Bonjour Alice.",
        "Comment je m'appelle ?",
        "Vous vous appelez Alice.",
    ]
    assert agent.get_state({"configurable": {"thread_id": "bob"}}).values == {}
