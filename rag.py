from __future__ import annotations
from typing import Optional
import io

import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

_embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
_vector_store: Optional[FAISS] = None


def ingest_pdf(file_bytes: bytes) -> int:
    global _vector_store
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    if not chunks:
        return 0

    if _vector_store is None:
        _vector_store = FAISS.from_texts(chunks, _embeddings)
    else:
        _vector_store.add_texts(chunks)

    return len(chunks)


def retrieve(query: str, k: int = 4) -> str:
    if _vector_store is None:
        return ""
    docs = _vector_store.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in docs)


def has_documents() -> bool:
    return _vector_store is not None


def clear_documents() -> None:
    global _vector_store
    _vector_store = None
