from langchain.tools import tool

@tool
def word_count(text: str) -> int:
    """Compte le nombre de mots dans un texte."""
    return len(text.split())

@tool
def char_count(text: str) -> int:
    """Compte le nombre de caractères dans un texte."""
    return len(text)
