from app.services.pinecone_service import retrieve_vendor_context

async def retrieve_context(state: dict) -> dict:
    docs = retrieve_vendor_context(state["vendor_id"])
    return {"retrieved_docs": docs}
