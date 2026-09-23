from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader

def load_pdf(path: str):
    """Charge un PDF et renvoie une liste de Documents."""
    return PyPDFLoader(path).load()

def load_txt(path: str):
    """Charge un fichier texte."""
    return TextLoader(path, encoding="utf-8").load()

def load_web(url: str):
    """Charge le contenu d'une page web."""
    return WebBaseLoader(url).load()
