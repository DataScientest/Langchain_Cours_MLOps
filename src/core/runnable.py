from .llm import llm
from langchain_core.messages import HumanMessage

def run_invoke(human_message: str):
    """Run a simple invoke call with a custom human message"""
    response = llm.invoke([HumanMessage(content=human_message)])
    return response.content

def run_batch(batch_human_messages: list[str]):
    """Run a batch of inputs with a list of human messages"""
    batch_inputs = [[HumanMessage(content=msg)] for msg in batch_human_messages]
    responses = llm.batch(batch_inputs)
    return [r.content for r in responses]

def run_stream(human_message: str):
    """Run a streaming generation with a custom human message"""
    print("Streaming response:")
    for chunk in llm.stream([HumanMessage(content=human_message)]):
        print(chunk.content, end="", flush=True)
    print("\n--- End of stream ---")

def run_with_retry(human_message: str):
    """Run with automatic retry and a custom human message"""
    safe_llm = llm.with_retry()
    response = safe_llm.invoke([HumanMessage(content=human_message)])
    return response.content
