import runpy

from src.documents.cleaners import clean_text
from src.documents.loaders import load_pdf
from src.documents.search import keyword_search
from src.documents.splitters import split_documents
from src.documents.tools import (
    clean_text_tool,
    count_tokens_tool,
    load_pdf_tool,
    read_pdf_excerpt_tool,
    search_keyword_tool,
)
from src.utils.token import count_tokens, truncate_to_tokens


def test_clean_text():
    assert clean_text("Titre\n  12 \nLigne    suivante") == "Titre Ligne suivante"
    assert clean_text("   ") == ""


def test_document_pipeline_on_course_pdf():
    docs = load_pdf("data/pdf/1.pdf")
    assert len(docs) == 10
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    chunks = split_documents(docs, chunk_size=800, chunk_overlap=150)

    assert len(chunks) > len(docs)
    assert all(len(c.page_content) <= 800 for c in chunks)
    assert count_tokens(chunks[0].page_content) > 0
    assert keyword_search(chunks, "McCarthy", k=2)


def test_document_tools():
    assert len(load_pdf_tool.invoke({"path": "data/pdf/3.pdf"})) == 5
    assert clean_text_tool.invoke({"text": "a   b"}) == "a b"
    assert count_tokens_tool.invoke({"text": "bonjour"}) > 0


def test_truncate_to_tokens():
    text = "un deux trois quatre cinq " * 100
    assert count_tokens(truncate_to_tokens(text, 50)) <= 50
    assert truncate_to_tokens("court", 50) == "court"


def test_read_pdf_excerpt_tool_is_bounded():
    excerpt = read_pdf_excerpt_tool.invoke({"path": "data/pdf/1.pdf"})
    assert excerpt.startswith("Intelligence artificielle")
    assert count_tokens(excerpt) <= 1500
    assert count_tokens(read_pdf_excerpt_tool.invoke({"path": "data/pdf/1.pdf", "max_tokens": 200})) <= 200


def test_chap3_script_runs(capsys):
    runpy.run_module("src.chap3_docs", run_name="__main__")
    out = capsys.readouterr().out
    assert "Nombre de chunks :" in out
    assert "--- Résultat 1 ---" in out
