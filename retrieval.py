import chromadb
from google import genai
from google.genai import types
from config import (
    GOOGLE_API_KEY, GEMINI_MODEL, EMBEDDING_MODEL, CHROMA_DIR,
    COLLECTION_NAME, TOP_K
)
from ingest import create_chunks

if not GOOGLE_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in your .env file.")

client = genai.Client(api_key=GOOGLE_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

def embed_texts(texts, task_type):
    """Create Gemini embeddings in small batches."""
    vectors = []
    for text in texts:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type)
        )
        vectors.append(response.embeddings[0].values)
    return vectors

def build_or_load_collection(force_rebuild=False):
    existing = [c if isinstance(c, str) else c.name for c in chroma_client.list_collections()]
    if COLLECTION_NAME in existing and force_rebuild:
        chroma_client.delete_collection(COLLECTION_NAME)
        existing.remove(COLLECTION_NAME)

    if COLLECTION_NAME in existing:
        return chroma_client.get_collection(COLLECTION_NAME)

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    chunks, metadatas, ids = create_chunks()
    if not chunks:
        raise RuntimeError("No documents found. Add PDF/TXT/MD files to the data folder.")
    embeddings = embed_texts(chunks, "RETRIEVAL_DOCUMENT")
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
        embeddings=embeddings
    )
    return collection

def answer_question(collection, question):
    query_vector = embed_texts([question], "RETRIEVAL_QUERY")[0]
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(TOP_K, collection.count())
    )
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    if not docs:
        return {"answer": "I could not find relevant information in the tourism documents.", "sources": []}

    context_parts, sources = [], []
    for doc, meta in zip(docs, metas):
        context_parts.append(doc)
        source = f'{meta.get("source", "Unknown")} (page {meta.get("page", "?")})'
        if source not in sources:
            sources.append(source)

    prompt = f"""
You are TravelMate, a helpful travel information assistant.
Answer the user's question using ONLY the context below.
If the answer is not clearly present, say: "I don't have enough information in the available tourism documents to answer that reliably."
Do not invent opening hours, ticket prices, transport schedules, safety advice, or booking availability.
Be clear and concise. Mention that visitors should verify changing details with official sources.

CONTEXT:
{chr(10).join(context_parts)}

QUESTION:
{question}
"""
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return {"answer": response.text or "I could not generate an answer.", "sources": sources}
