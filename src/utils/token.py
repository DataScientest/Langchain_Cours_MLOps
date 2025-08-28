import tiktoken 

ENCODING = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str, margin: int = 5) -> int:
    return len(ENCODING.encode(text)) + margin