from typing import TypedDict, List

class VendorGraphState(TypedDict):
    vendor_id: str
    vendor_name: str
    retrieved_docs: List[str]
    final_assessment: str
    