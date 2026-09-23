from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.chains import summary_chain, translation_chain
from src.agents.doc_agent import doc_agent, chat_agent

app = FastAPI(title="LangChain Course API", version="4.0.0")

class TextInput(BaseModel):
    text: str

class AgentInput(BaseModel):
    file_path: str
    query: str

class ChatInput(BaseModel):
    session_id: str
    query: str

class HistoryInput(BaseModel):
    session_id: str

@app.post("/summary")
def summary(input: TextInput):
    result = summary_chain.invoke({"input": input.text})
    return {"summary": result.summary}

@app.post("/translate")
def translate(input: TextInput):
    result = translation_chain.invoke({"input": input.text})
    return {"translated_text": result.translated_text}

@app.post("/agent")
def run_agent(input: AgentInput):
    if not input.file_path:
        raise HTTPException(status_code=400, detail="Le chemin du fichier est obligatoire.")

    result = doc_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Charge le document situé ici : {input.file_path}. "
                    f"Ensuite, réponds à cette question : {input.query}"
                ),
            }
        ]
    })
    return {"response": result["messages"][-1].content}

@app.post("/chat")
def chat(input: ChatInput):
    result = chat_agent.invoke(
        {"messages": [{"role": "user", "content": input.query}]},
        config={"configurable": {"thread_id": input.session_id}},
    )
    return {"response": result["messages"][-1].content}

@app.post("/history")
def history(input: HistoryInput):
    state = chat_agent.get_state({"configurable": {"thread_id": input.session_id}})
    messages = state.values.get("messages", [])
    return {"history": [{"type": m.type, "content": m.content} for m in messages]}
