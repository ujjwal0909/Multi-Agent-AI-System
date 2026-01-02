import os
import json
import faiss
import numpy as np


class FaissStore:
    def __init__(self, index_path: str, meta_path: str, dim: int):
        self.index_path = index_path
        self.meta_path = meta_path
        self.dim = dim
        self.index = None
        self.meta = []  # list of dicts: {source, chunk_id, text}

    def create(self):
        # cosine similarity via normalized vectors + inner product
        self.index = faiss.IndexFlatIP(self.dim)
        self.meta = []

    def add(self, vectors: np.ndarray, metadatas: list[dict]):
        self.index.add(vectors.astype(np.float32))
        self.meta.extend(metadatas)

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.meta_path):
            raise FileNotFoundError(
                "RAG index not found. Run ingestion first to create data/index/docs.index and docs.meta.json"
            )
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.meta = json.load(f)

    def search(self, query_vec: np.ndarray, top_k: int = 6):
        scores, idxs = self.index.search(query_vec.astype(np.float32), top_k)
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx == -1:
                continue
            item = dict(self.meta[idx])
            item["score"] = float(score)
            results.append(item)
        return results
