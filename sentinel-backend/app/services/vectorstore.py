# app/services/vectorstore.py
import uuid
from typing import List
from cohere import Client
from pinecone import Pinecone
from app.config.settings import settings

co = Client(settings.COHERE_API_KEY)
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

def embed_and_upsert(vendor_id: str, docs: List[str]):
    """Embed and upsert multiple docs for a vendor into Pinecone."""
    for doc in docs:
        chunks = chunk_text(doc)
        resp = co.embed(texts=chunks, model="embed-multilingual-v3.0", input_type="search_document")
        vectors = resp.embeddings
        upserts = [
            {
                "id": f"{vendor_id}-{uuid.uuid4()}",
                "values": vec,
                "metadata": {"vendor_id": vendor_id, "text": chunk}
            }
            for vec, chunk in zip(vectors, chunks)
        ]
        index.upsert(vectors=upserts, namespace=vendor_id)

def query_vendor(vendor_id: str, query: str, top_k: int = 10):
    """Query Pinecone for vendor-specific docs."""
    qvec = co.embed(texts=[query], model="embed-multilingual-v3.0", input_type="search_query").embeddings[0]
    res = index.query(vector=qvec, namespace=vendor_id, top_k=top_k, include_metadata=True)

    texts = [m.metadata["text"] for m in res.matches]
    evidences = [
        {
            "text": m.metadata.get("text", ""),
            "score": float(m.score),
            "doc_type": m.metadata.get("doc_type"),
            "source_id": m.id,
        } for m in res.matches
    ]


    return texts, evidences