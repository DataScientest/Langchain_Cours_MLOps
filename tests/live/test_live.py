"""Tests avec un vrai modèle : RUN_LIVE=1 uv run pytest -m live (GROQ_API_KEY requis)."""

import importlib.util

import pytest

pytestmark = pytest.mark.live


def _requires(module):
    return pytest.mark.skipif(importlib.util.find_spec(module) is None, reason=f"{module} absent de ce chapitre")


def test_llm_answers():
    from src.core.llm import llm

    assert llm.invoke("Réponds uniquement par OK.").content.strip()


@_requires("src.core.chains")
def test_structured_output():
    from src.core.chains import classification_chain

    result = classification_chain.invoke({"input": "Kubernetes orchestre des conteneurs."})
    assert 0 <= result.confidence <= 1


@_requires("src.agents.doc_agent")
def test_chat_agent_memory():
    from src.agents.doc_agent import chat_agent

    config = {"configurable": {"thread_id": "live-alice"}}
    chat_agent.invoke({"messages": [{"role": "user", "content": "Je m'appelle Alice."}]}, config=config)
    result = chat_agent.invoke({"messages": [{"role": "user", "content": "Quel est mon prénom ?"}]}, config=config)
    assert "Alice" in result["messages"][-1].content
