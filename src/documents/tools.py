from langchain.tools import tool
from .loaders import load_pdf
from .cleaners import clean_text
from .search import keyword_search
from src.utils.token import count_tokens, truncate_to_tokens

@tool
def load_pdf_tool(path: str):
    """Loads a PDF and returns the extracted documents."""
    return load_pdf(path)

@tool
def clean_text_tool(text: str) -> str:
    """Cleans raw text before analysis."""
    return clean_text(text)

@tool
def count_tokens_tool(text: str) -> int:
    """Counts the number of tokens in a text."""
    return count_tokens(text)

@tool
def search_keyword_tool(chunks: list, query: str, k: int = 3) -> list:
    """Searches for a keyword in a list of chunks."""
    return keyword_search(chunks, query, k=k)

@tool
def read_pdf_excerpt_tool(path: str, max_tokens: int = 1500) -> str:
    """Read a PDF and return a cleaned excerpt (start of the document) for analysis."""
    text = " ".join(clean_text(doc.page_content) for doc in load_pdf(path))
    return truncate_to_tokens(text, max_tokens)
