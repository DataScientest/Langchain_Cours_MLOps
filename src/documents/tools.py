from typing import List, Dict
from langchain_core.documents import Document
from langchain.tools import tool
from .loaders import load_pdf, load_txt, load_markdown
from .cleaners import clean_text
from .splitters import split_documents
from .search import keyword_search

# === CHARGEMENT ===

@tool("load_pdf_tool")
def load_pdf_tool(path: str) -> List[Document]:
    return load_pdf(path)

@tool("load_txt_tool")
def load_txt_tool(path: str) -> List[Document]:
    return load_txt(path)

@tool("load_markdown_tool")
def load_markdown_tool(path: str) -> List[Document]:
    return load_markdown(path)

# === NETTOYAGE ===

@tool("clean_text_tool")
def clean_text_tool(text: str) -> str:
    return clean_text(text)

# === SPLITTING ===

@tool("split_texts_tool")
def split_texts_tool(input_data: Dict[str, List[Document]]) -> List[Document]:
    docs = input_data["docs"]
    return split_documents(docs, max_tokens=600, overlap_sentences=2)

# === RECHERCHE SIMPLE ===

DOC_STORE: List[Document] = [] 

@tool("set_corpus_tool")
def set_corpus_tool(input_data: Dict[str, List[Document]]) -> str:
    global DOC_STORE
    docs = input_data["docs"]
    DOC_STORE = docs
    return f"Corpus initialisé avec {len(docs)} documents."

@tool("search_keyword_tool")
def search_keyword_tool(query: str) -> List[str]:
    return keyword_search(DOC_STORE, query, k=3)
