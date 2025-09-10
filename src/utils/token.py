import tiktoken

ENCODING = tiktoken.get_encoding("cl100k_base")

def count_tokens(data, margin: int = 5) -> int:
    """Compte les tokens dans une chaîne ou une liste de messages."""
    if isinstance(data, str):
        text = data
    elif isinstance(data, list):
        text = " ".join([msg.content for msg in data])
    else:
        text = str(data)
    return len(ENCODING.encode(text)) + margin
