from fastapi.testclient import TestClient
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from pydantic import BaseModel

from src.agents.doc_agent import TOOLS
from src.api import main
from tests.fakes import ToolCallingFakeChatModel

client = TestClient(main.app)


def test_summary_and_translate():
    summary = client.post("/summary", json={"text": "Un long texte."})
    translate = client.post("/translate", json={"text": "Bonjour"})

    assert summary.status_code == 200 and set(summary.json()) == {"summary"}
    assert translate.status_code == 200 and set(translate.json()) == {"translated_text"}


def test_agent_endpoint_calls_pdf_tool(monkeypatch):
    model = ToolCallingFakeChatModel(
        messages=iter([
            AIMessage(
                content="",
                tool_calls=[{"name": "load_pdf_tool", "args": {"path": "data/pdf/1.pdf"}, "id": "t1"}],
            ),
            AIMessage(content="Le document traite de l'intelligence artificielle."),
        ])
    )
    agent = create_agent(model, tools=TOOLS)
    monkeypatch.setattr(main, "doc_agent", agent)

    response = client.post("/agent", json={"file_path": "data/pdf/1.pdf", "query": "give me the subject"})

    assert response.status_code == 200
    assert response.json() == {"response": "Le document traite de l'intelligence artificielle."}


def test_agent_endpoint_rejects_empty_path():
    response = client.post("/agent", json={"file_path": "", "query": "?"})
    assert response.status_code == 400


def test_chat_memory_and_history():
    client.post("/chat", json={"session_id": "alice", "query": "Bonjour, je m'appelle Alice."})
    client.post("/chat", json={"session_id": "bob", "query": "Bonjour, je m'appelle Bob."})
    response = client.post("/chat", json={"session_id": "alice", "query": "Quel est mon nom ?"})

    assert response.status_code == 200
    assert "Alice" in response.json()["response"]
    assert "Bob" not in response.json()["response"]

    history = client.post("/history", json={"session_id": "alice"}).json()["history"]
    assert [m["type"] for m in history] == ["human", "ai", "human", "ai"]
    assert history[0]["content"] == "Bonjour, je m'appelle Alice."
    assert client.post("/history", json={"session_id": "inconnu"}).json() == {"history": []}


def test_agent_structured_response_format():
    class DocAnswer(BaseModel):
        answer: str
        source_used: str

    model = ToolCallingFakeChatModel(
        messages=iter([
            AIMessage(
                content="",
                tool_calls=[{
                    "name": "DocAnswer",
                    "args": {"answer": "L'IA", "source_used": "data/pdf/1.pdf"},
                    "id": "s1",
                }],
            ),
        ])
    )
    agent = create_agent(model, tools=TOOLS, response_format=DocAnswer)

    result = agent.invoke({"messages": [{"role": "user", "content": "Sujet ?"}]})

    assert result["structured_response"] == DocAnswer(answer="L'IA", source_used="data/pdf/1.pdf")
    assert any(isinstance(m, ToolMessage) for m in result["messages"])
