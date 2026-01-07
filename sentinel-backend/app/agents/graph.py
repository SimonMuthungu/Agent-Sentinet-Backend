# graph builder

from langgraph.graph import StateGraph, END
from app.agents.state import VendorGraphState
from app.agents.nodes.ingestion import ingest_vendor
from app.agents.nodes.retrieval import retrieve_context
from app.agents.nodes.reasoning import reason_over_context
from app.agents.nodes.guardrails import guardrail_check
from app.agents.nodes.synthesis import synthesize_response
from app.agents.nodes.review import human_review
from app.api.escalations import escalation_router

def build_graph():
    graph = StateGraph(VendorGraphState)

    graph.add_node("ingest", ingest_vendor)
    graph.add_node("retrieve", retrieve_context)
    graph.add_node("reason", reason_over_context)
    graph.add_node("guardrails", guardrail_check)
    graph.add_node("synthesize", synthesize_response)
    graph.add_node("review", human_review)

    graph.set_entry_point("ingest")

    graph.add_edge("ingest", "retrieve")
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", "guardrails")

    graph.add_conditional_edges(
        "guardrails",
        escalation_router,
        {
            "review": "review",
            "synthesize": "synthesize",
        }
    )

    graph.add_edge("synthesize", END)
    graph.add_edge("review", END)

    return graph.compile()

executor = build_graph()
