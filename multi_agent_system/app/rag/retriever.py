import numpy as np
from sentence_transformers import SentenceTransformer
from app.rag.vectorstore import FaissStore

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class Retriever:
    def __init__(self, index_path="data/index/docs.index", meta_path="data/index/docs.meta.json"):
        self.embedder = SentenceTransformer(EMBED_MODEL)

        # MiniLM output dim is 384, but we keep it flexible:
        self.store = FaissStore(index_path=index_path, meta_path=meta_path, dim=384)
        self.store.load()

    def retrieve(self, query: str, top_k: int = 6):
        q = self.embedder.encode([query], normalize_embeddings=True)
        q = np.array(q, dtype=np.float32)
        return self.store.search(q, top_k=top_k)
