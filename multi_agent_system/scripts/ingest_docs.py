from app.rag.ingest import ingest_docs

if __name__ == "__main__":
    stats = ingest_docs()
    print("Ingestion complete:", stats)
