from dotenv import load_dotenv

# Load .env first: WebBaseLoader reads USER_AGENT when it is imported.
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader

def load_pdf(path: str):
    """Loads a PDF and returns a list of Documents."""
    return PyPDFLoader(path).load()

def load_txt(path: str):
    """Loads a text file."""
    return TextLoader(path, encoding="utf-8").load()

def load_web(url: str):
    """Loads the content of a web page."""
    return WebBaseLoader(url).load()
