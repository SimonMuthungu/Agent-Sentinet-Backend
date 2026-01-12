# app/agents/nodes/guardrails.py
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

RULES = [
    {
        "id": "NDA-001",
        "desc": "NDA must have mutual signatures and no unilateral disclosure clauses",
        "check": lambda state: _check_nda_integrity(state),
        "severity": "high",
    },
    {
        "id": "SOC2-001",
        "desc": "SOC2 must be auditor-verified (no self-certification)",
        "check": lambda state: _check_soc2_audit(state),
        "severity": "critical",
    },
    {
        "id": "ENC-001",
        "desc": "Encryption at rest and in transit must be explicitly stated",
        "check": lambda state: _check_encryption_mentions(state),
        "severity": "medium",
    },
]

def _any_text_contains(state: Dict, needles: List[str]) -> bool:
    for t in state.get("retrieved_docs", []):
        if any(n.lower() in t.lower() for n in needles):
            return True
    return False

def _check_nda_integrity(state: Dict) -> Dict | None:
    risky = _any_text_contains(state, ["trusted partners", "marketing purposes", "unilateral", "no company signature"])
    ok_signatures = _any_text_contains(state, ["Signed:", "Signature", "Both parties"])
    if risky or not ok_signatures:
        return {"rule_id": "NDA-001", "description": "NDA integrity concerns", "severity": "high", "evidence_ref": "NDA"}
    return None

def _check_soc2_audit(state: Dict) -> Dict | None:
    bad = _any_text_contains(state, ["self-certifies", "no independent auditor", "no external validation"])
    good = _any_text_contains(state, ["Type II", "independent audit", "SecureAudit LLP", "CPA"])
    if bad or not good:
        return {"rule_id": "SOC2-001", "description": "SOC2 audit verification missing", "severity": "critical", "evidence_ref": "SOC2"}
    return None

def _check_encryption_mentions(state: Dict) -> Dict | None:
    has_enc = _any_text_contains(state, ["encryption at rest", "encryption in transit", "TLS", "AES"])
    if not has_enc:
        return {"rule_id": "ENC-001", "description": "Encryption mentions missing", "severity": "medium", "evidence_ref": "policy"}
    return None

def guardrail_check(state: Dict) -> Dict:
    violations = []
    for rule in RULES:
        res = rule["check"](state)
        if res:
            violations.append(res)

    escalate = any(v["severity"] in ("high", "critical") for v in violations)

    logger.info("guardrails.completed", extra={
        "vendor_id": state["vendor_id"],
        "violations": [v["rule_id"] for v in violations],
        "escalate": escalate,
    })

    return {
        "policy_violations": violations,
        "escalate": escalate,
    }