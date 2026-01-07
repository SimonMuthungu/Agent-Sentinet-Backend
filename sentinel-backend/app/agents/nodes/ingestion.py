async def ingest_vendor(state: dict) -> dict:
    """
    Entry node.
    Ensures required fields exist and normalizes state.
    """
    return {
        "vendor_id": state["vendor_id"],
        "vendor_name": state.get("vendor_name", "Unknown Vendor"),
        "retrieved_docs": [],
        "final_assessment": "",
    }
