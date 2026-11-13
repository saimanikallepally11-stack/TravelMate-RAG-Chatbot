from pathlib import Path
from pypdf import PdfReader
from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def load_documents():
    """Load PDF, TXT and Markdown files from the data directory."""
    documents = []
    for path in Path(DATA_DIR).glob("*"):
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            reader = PdfReader(str(path))
            for page_no, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    documents.append({
                        "text": text,
                        "source": path.name,
                        "page": page_no
                    })
        elif suffix in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8")
            if text.strip():
                documents.append({"text": text, "source": path.name, "page": 1})
    return documents

def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Simple character-based chunking with overlap."""
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

def create_chunks():
    chunks, metadatas, ids = [], [], []
    for doc_index, doc in enumerate(load_documents()):
        for chunk_index, chunk in enumerate(split_text(doc["text"])):
            chunks.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "page": int(doc["page"])
            })
            ids.append(f"doc{doc_index}_chunk{chunk_index}")
    return chunks, metadatas, ids
