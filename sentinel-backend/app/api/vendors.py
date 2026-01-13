from fastapi import APIRouter
from app.agents.graph_runner import run_vendor_evaluation
from app.persistence.db import supabase
from app.observability.logging import logger
from app.services.vectorstore import query_vendor
from app.agents.state import VendorGraphState
from app.agents.graph import executor



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


# @router.post("/{vendor_id}/review")
# async def review_vendor(vendor_id: str):
#     initial_state: VendorGraphState = {
#         "vendor_id": vendor_id,
#         "vendor_name": get_vendor_name(vendor_id),
#         "query": "Assess vendor compliance risk",
#     }

#     contexts = query_vendor(vendor_id, "Assess vendor compliance risk")
#     result = await run_vendor_evaluation(vendor_id, contexts)
#     return result


@router.post("/{vendor_id}/review")
async def review_vendor(vendor_id: str):
    initial_state: VendorGraphState = {
        "vendor_id": vendor_id,
        "vendor_name": get_vendor(vendor_id)["vendor"]["name"],
        "query": "Assess vendor compliance risk",
    }

    print('Have received user input, Now running the agent...')

    result_state = await executor.ainvoke(initial_state)  # LangGraph executor
    # Return only synthesis + guardrails + review signals

    supabase.table("vendor_runs").insert({
        "vendor_id": vendor_id,
        "decision": result_state.get("decision"),
        "confidence": result_state.get("confidence"),
        "final_assessment": result_state.get("final_assessment"),
        "recommended_actions": result_state.get("recommended_actions", []),
        "policy_violations": result_state.get("policy_violations", []),
        "human_review_required": result_state.get("human_review_required", False),
        "full_state": result_state,  # optional: store everything
    }).execute()


    print('Done running the agent, Now returning the result...')

    logger.info("Graph final output", extra={"vendor_id": vendor_id, "result_state": result_state})
    # print("Graph final output:", result_state)


    return {
        "vendor_id": vendor_id,
        "decision": result_state.get("decision"),
        "confidence": result_state.get("confidence"),
        "final_assessment": result_state.get("final_assessment"),
        "recommended_actions": result_state.get("recommended_actions", []),
        "policy_violations": result_state.get("policy_violations", []),
        "human_review_required": result_state.get("human_review_required", False),
        "retrieved_count": len(result_state.get("retrieved_docs", [])),
    }


@router.get("/{vendor_id}/reports")
def list_vendor_runs(vendor_id: str):
    res = (
        supabase.table("vendor_runs")
        .select("*")
        .eq("vendor_id", vendor_id)
        .order("run_timestamp", desc=True)
        .execute()
    )
    return res.data