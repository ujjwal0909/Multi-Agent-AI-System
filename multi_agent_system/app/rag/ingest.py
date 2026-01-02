from pathlib import Path
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

from app.rag.splitter import chunk_text
from app.rag.vectorstore import FaissStore

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def read_pdf(path: str, max_pages: int = 25) -> str:
    """
    Low-RAM PDF reader: only read first max_pages pages.
    """
    reader = PdfReader(path)
    out = []
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        out.append(page.extract_text() or "")
    return "\n".join(out)


def read_text_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def ingest_docs(
    docs_dir: str = "data/docs",
    out_dir: str = "data/index",
    max_pages_per_pdf: int = 25,
    max_total_chunks: int = 800
):
    """
    Ingest documents from data/docs into a FAISS index saved in data/index.
    Designed for 8GB RAM laptops:
    - limits PDF pages
    - limits chunks per document (in splitter)
    - limits total chunks overall
    """
    docs_dir = Path(docs_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not docs_dir.exists():
        raise RuntimeError("data/docs folder not found. Create it and add files (pdf/txt/md).")

    embedder = SentenceTransformer(EMBED_MODEL)

    all_chunks: List[Dict] = []
    supported = {".pdf", ".txt", ".md"}

    for file in docs_dir.glob("*"):
        if file.suffix.lower() not in supported:
            continue

        if file.suffix.lower() == ".pdf":
            text = read_pdf(str(file), max_pages=max_pages_per_pdf)
        else:
            text = read_text_file(str(file))

        chunks = chunk_text(text)  # already capped by splitter.max_chunks
        for i, c in enumerate(chunks):
            all_chunks.append({"source": file.name, "chunk_id": i, "text": c})

        # hard stop if too many chunks overall
        if len(all_chunks) >= max_total_chunks:
            all_chunks = all_chunks[:max_total_chunks]
            break

    if not all_chunks:
        raise RuntimeError("No supported docs found in data/docs (pdf/txt/md). Add files and retry.")

    texts = [c["text"] for c in all_chunks]

    # embeddings (normalized so inner product = cosine similarity)
    vecs = embedder.encode(texts, normalize_embeddings=True, batch_size=32)
    vecs = np.array(vecs, dtype=np.float32)
    dim = vecs.shape[1]

    store = FaissStore(
        index_path=str(out_dir / "docs.index"),
        meta_path=str(out_dir / "docs.meta.json"),
        dim=dim
    )
    store.create()
    store.add(vecs, all_chunks)
    store.save()

    return {
        "files_indexed": len(set(c["source"] for c in all_chunks)),
        "chunks": len(all_chunks),
        "dim": dim,
        "out_dir": str(out_dir)
    }
