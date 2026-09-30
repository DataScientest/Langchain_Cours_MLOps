from typing import List
from langchain_core.documents import Document

def keyword_search(docs: List[Document], query: str, k: int = 3) -> List[str]:
    matches = []
    query_lower = query.lower()

    for doc in docs:
        if query_lower in doc.page_content.lower():
            matches.append(doc.page_content[:500])

    return matches[:k]
