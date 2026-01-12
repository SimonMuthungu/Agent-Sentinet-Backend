# app/agents/state.py
from typing import TypedDict, List, Literal, Optional

class VendorGraphState(TypedDict, total=False):
    vendor_id: str
    vendor_name: str

    # Retrieval
    query: str
    retrieved_docs: List[str]
    retrieved_evidence: List[dict]  # [{text, score, doc_type, source_id}]

    # Reasoning
    extracted_risks: List[dict]  # [{category, severity, description, evidence_ref}]
    framework_mapping: List[dict]  # [{framework, control, status, evidence_ref}]
    reasoning_notes: str

    # Guardrails
    policy_violations: List[dict]  # [{rule_id, description, severity, evidence_ref}]
    escalate: bool

    # Synthesis
    decision: Literal["APPROVED", "REVIEW_REQUIRED", "BLOCKED"]
    confidence: float
    final_assessment: str
    recommended_actions: List[str]

    # Review
    human_review_required: bool
    reviewer_notes: Optional[str]