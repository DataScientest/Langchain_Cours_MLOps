import re

def clean_text(text: str) -> str:
    if not text or not text.strip():
        return ""

    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
