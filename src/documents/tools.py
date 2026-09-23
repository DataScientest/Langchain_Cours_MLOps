from langchain.tools import tool
from .loaders import load_pdf
from .cleaners import clean_text
from .search import keyword_search
from src.utils.token import count_tokens

@tool
def load_pdf_tool(path: str):
    """Charge un PDF et renvoie les documents extraits."""
    return load_pdf(path)

@tool
def clean_text_tool(text: str) -> str:
    """Nettoie un texte brut avant analyse."""
    return clean_text(text)

@tool
def count_tokens_tool(text: str) -> int:
    """Compte le nombre de tokens d'un texte."""
    return count_tokens(text)

@tool
def search_keyword_tool(chunks: list, query: str, k: int = 3) -> list:
    """Recherche un mot-clé dans une liste de chunks."""
    return keyword_search(chunks, query, k=k)
