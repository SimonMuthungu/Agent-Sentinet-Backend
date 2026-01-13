import google.generativeai as genai
from app.config.settings import settings
from app.observability.logging import logger

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def synthesize(context: str, vendor_name: str) -> str:
    prompt = f"""
    Assess vendor risk.

    Vendor: {vendor_name}
    Context:
    {context}

    Return a concise compliance risk summary.
    """
    response = model.generate_content(prompt)
    return response.text


async def gemini_structured_analysis(vendor_name: str, docs: list) -> dict:
    context = "\n\n".join(docs[:50])  # cap for prompt size
    prompt = f"""
You are a vendor risk analyst. Analyze the following vendor documents and produce structured JSON:
- extracted_risks: list of {{category: one of [legal, security, privacy, operational], severity: one of [low, medium, high, critical], description, evidence_ref}}
- framework_mapping: list of {{framework: one of [SOC2, ISO27001, GDPR], control, status: one of [met, partial, missing], evidence_ref}}
- reasoning_notes: concise explanation of the most material risks

Vendor: {vendor_name}
Context:
{context}

Return only valid JSON. No prose.
CRITICAL: Return ONLY valid JSON. Do not include any prose, comments, or explanations.
"""
    # Gemini Python SDK generate_content is sync; call in thread if you need true async
    response = model.generate_content(prompt)
    logger.info("Gemini raw response", extra={"vendor": vendor_name, "raw": response.text})
    print("Gemini raw response:", response.text)

    # For safety, parse JSON (assume response.text is valid JSON)
    import json, re

    raw = (response.text or "").strip()               # remove closing ```

    logger.info("Gemini raw response", extra={"raw": raw})

    if not raw:
        # log and return a safe default
        logger.error("Gemini returned empty response", extra={"vendor": vendor_name})
        return {"extracted_risks": [], "framework_mapping": [], "reasoning_notes": ""}

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z0-9]*\n?", "", raw)   # remove opening ```json
        raw = re.sub(r"\n?```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Invalid JSON from Gemini", extra={"raw": raw})
        return {"extracted_risks": [], "framework_mapping": [], "reasoning_notes": raw}


# app/services/llm.py (append)
async def gemini_executive_synthesis(
    vendor_name: str,
    extracted_risks: list,
    framework_mapping: list,
    policy_violations: list,
    retrieved_evidence: list,
) -> dict:
    import json
    prompt = f"""
You are producing an executive risk memo.

Inputs (JSON):
extracted_risks: {json.dumps(extracted_risks)[:6000]}
framework_mapping: {json.dumps(framework_mapping)[:6000]}
policy_violations: {json.dumps(policy_violations)[:4000]}
retrieved_evidence: {json.dumps(retrieved_evidence)[:4000]}

Output strictly JSON with keys:
- decision: one of ["APPROVED","REVIEW_REQUIRED","BLOCKED"]
- confidence: float between 0 and 1
- summary: concise memo (<= 200 words) citing key evidence
- recommended_actions: list of concrete steps (<= 5)

Decision policy:
- If any critical violation -> "BLOCKED"
- Else if any high violations or missing SOC2 audit -> "REVIEW_REQUIRED"
- Else -> "APPROVED"
Confidence reflects evidence density and consistency.
"""
    response = model.generate_content(prompt)
    raw = (response.text or "").strip()
    if not raw:
        logger.error("Gemini returned empty executive synthesis", extra={"vendor": vendor_name})
        return {"decision": "REVIEW_REQUIRED", "confidence": 0.0,
                "summary": "", "recommended_actions": []}

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z0-9]*\n?", "", raw)   # remove opening ```json
        raw = re.sub(r"\n?```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Invalid JSON from Gemini executive synthesis", extra={"raw": raw})
        return {"decision": "REVIEW_REQUIRED", "confidence": 0.0,
                "summary": raw, "recommended_actions": []}