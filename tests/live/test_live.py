"""Tests against the real model: RUN_LIVE=1 uv run pytest -m live (requires GROQ_API_KEY)."""

import importlib.util

import pytest

pytestmark = pytest.mark.live


def _requires(module):
    return pytest.mark.skipif(importlib.util.find_spec(module) is None, reason=f"{module} not part of this chapter")


def test_llm_answers():
    from src.core.llm import llm

    assert llm.invoke("Réponds uniquement par OK.").content.strip()


@_requires("src.core.chains")
@pytest.mark.parametrize("attempt", range(3))
def test_structured_output_chains(attempt):
    from src.core.chains import classification_chain, summary_chain, translation_chain

    text = "Artificial intelligence helps machines solve problems and analyze data."
    assert 0 <= classification_chain.invoke({"input": text}).confidence <= 1
    assert summary_chain.invoke({"input": text}).summary
    assert translation_chain.invoke({"input": "Bonjour, comment allez-vous ?"}).translated_text


@_requires("src.agents.doc_agent")
def test_doc_agent_reads_course_pdf():
    from langchain_core.messages import ToolMessage

    from src.agents.doc_agent import doc_agent

    result = doc_agent.invoke({
        "messages": [{"role": "user", "content": "Charge le PDF data/pdf/1.pdf puis explique son sujet principal."}]
    })
    assert any(isinstance(m, ToolMessage) and m.name == "read_pdf_excerpt_tool" for m in result["messages"])
    assert "intelligence artificielle" in result["messages"][-1].content.lower()


@_requires("src.agents.doc_agent")
def test_doc_agent_structured_response():
    import os

    from langchain.agents import create_agent
    from langchain.agents.structured_output import ToolStrategy
    from pydantic import BaseModel

    from src.agents.doc_agent import TOOLS

    class DocAnswer(BaseModel):
        answer: str
        source_used: str

    agent = create_agent(
        model=os.getenv("CHAT_MODEL", "groq:openai/gpt-oss-120b"),
        tools=TOOLS,
        response_format=ToolStrategy(DocAnswer),
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "Charge le PDF data/pdf/3.pdf puis donne son sujet."}]})
    assert isinstance(result["structured_response"], DocAnswer)


@_requires("src.agents.doc_agent")
def test_chat_agent_memory():
    from src.agents.doc_agent import chat_agent

    config = {"configurable": {"thread_id": "live-alice"}}
    chat_agent.invoke({"messages": [{"role": "user", "content": "Je m'appelle Alice."}]}, config=config)
    result = chat_agent.invoke({"messages": [{"role": "user", "content": "Quel est mon prénom ?"}]}, config=config)
    assert "Alice" in result["messages"][-1].content
