from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Vendor(BaseModel):
    id: str
    name: str
    risk_score: Optional[float] = None
    last_evaluated_at: Optional[datetime] = None
