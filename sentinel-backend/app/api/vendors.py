from fastapi import APIRouter
from app.agents.graph_runner import run_vendor_evaluation
from app.persistence.db import supabase
from app.observability.logging import logger


router = APIRouter()


@router.post("/{vendor_id}/evaluate")
async def evaluate_vendor(vendor_id: str, query: str):
    """
    Runs the agent against a vendor.
    """
    return await run_vendor_evaluation(vendor_id, query)


@router.get("/")
def list_vendors():
    """
    Used by frontend Vendors table.
    """
    res = (
        supabase
        .table("vendors")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    # logger.info(f"Supabase vendors response: {res}")
    # logger.info(f"Supabase vendors data: {res.data}")
    return res.data


@router.get("/{vendor_id}")
def get_vendor(vendor_id: str):
    vendor = (
        supabase
        .table("vendors")
        .select("*")
        .eq("id", vendor_id)
        .single()
        .execute()
    )

    docs = (
        supabase
        .table("vendor_documents")
        .select("*")
        .eq("vendor_id", vendor_id)
        .execute()
    )

    # logger.info(f"Vendor {vendor_id}: {vendor.data}")
    # logger.info(f"Vendor {vendor_id} docs: {docs.data}")

    return {
        "vendor": vendor.data,
        "documents": docs.data
    }
