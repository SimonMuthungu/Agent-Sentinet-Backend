from pinecone import Pinecone
from app.config.settings import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX)

def retrieve_vendor_context(vendor_id: str):
    results = index.query(
        vector=[0.0] * 1536,
        top_k=5,
        include_metadata=True
    )
    return [m["metadata"]["text"] for m in results["matches"]]
