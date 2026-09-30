import tiktoken

ENCODING = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(ENCODING.encode(text))

def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Return the beginning of the text, limited to max_tokens tokens."""
    return ENCODING.decode(ENCODING.encode(text)[:max_tokens])
