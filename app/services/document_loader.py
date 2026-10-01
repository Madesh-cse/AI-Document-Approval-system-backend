from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

def load_document(file_path: str):
    path = Path(file_path)
    if not path.exists():
        f"Document not found {file_path}"
    extension = path.suffix.lower()
    if extension == ".pdf":
        loader = PyPDFLoader(str(path))
    
    elif extension == ".txt":
       loader = TextLoader(str(path), encoding="utf-8")
    
    else:
        raise ValueError(f"Unsupport document type: {extension}")
    
    #  load a data into document object
    return loader.load()
    

