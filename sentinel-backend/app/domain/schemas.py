from pydantic import BaseModel

class VendorCreate(BaseModel):
    name: str

class EvaluationRequest(BaseModel):
    vendor_id: str
