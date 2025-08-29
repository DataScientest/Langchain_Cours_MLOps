import re

def clean_text(text: str) -> str:
    if not text or text.strip() == "":
        return ""

    # Supprimer les numéros de page isolés (ex: "12" sur une ligne seule)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # Normaliser les espaces (un seul espace entre les mots)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()