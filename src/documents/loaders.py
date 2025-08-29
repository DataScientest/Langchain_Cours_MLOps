from langchain_community.document_loaders import PyPDFLoader, TextLoader

def load_pdf(path: str):
    loader = PyPDFLoader(path)
    return loader.load()

def load_txt(path: str, encoding: str = "utf-8"):
    loader = TextLoader(path, encoding=encoding)
    return loader.load()

def load_markdown(path: str, encoding: str = "utf-8"):
    return load_txt(path, encoding=encoding)
