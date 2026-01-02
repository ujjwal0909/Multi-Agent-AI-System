def chunk_text(
    text: str,
    chunk_size: int = 450,
    overlap: int = 80,
    max_chunks: int = 300
):
    """
    Low-RAM safe chunking:
    - smaller chunks help local models
    - max_chunks prevents memory blowups
    """
    text = (text or "").replace("\r", "")
    chunks = []
    start = 0
    n = len(text)

    while start < n and len(chunks) < max_chunks:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0
        if start >= n:
            break

    return chunks
