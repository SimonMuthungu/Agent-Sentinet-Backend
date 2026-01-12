# app/agents/nodes/retrieval.py
import logging
from typing import Dict
from app.services.vectorstore import query_vendor

logger = logging.getLogger(__name__)

def retrieve_context(state: Dict) -> Dict:
    """Graph node: retrieve relevant docs for a vendor query."""
    vendor_id = state["vendor_id"]
    query = state.get("query", "Assess vendor compliance risk")

    texts, evidences = query_vendor(vendor_id, query, top_k=12)

    logger.info("retrieval.completed", extra={
        "vendor_id": vendor_id,
        "count": len(texts),
    })

    return {
        "retrieved_docs": texts,
        "retrieved_evidence": evidences,
        "query": query,
    }