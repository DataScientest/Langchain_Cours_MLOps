from src.documents.loaders import load_pdf
from src.documents.cleaners import clean_text
from src.documents.splitters import split_documents
from src.documents.search import keyword_search
from src.utils.token import count_tokens

docs = load_pdf("data/pdf/1.pdf")

for doc in docs:
    doc.page_content = clean_text(doc.page_content)

chunks = split_documents(docs, chunk_size=800, chunk_overlap=150)

print("Nombre de chunks :", len(chunks))
print("Tokens du premier chunk :", count_tokens(chunks[0].page_content))

results = keyword_search(chunks, "McCarthy", k=2)
for i, result in enumerate(results, 1):
    print(f"\n--- Résultat {i} ---")
    print(result)
