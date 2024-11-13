from pydantic import BaseModel
from typing import Optional

class CBC(BaseModel):
    age: float
    sex: str
    HGB: float
    WBC: float
    RBC: float
    MCV: float
    PLT: float
    ground_truth: Optional[int]
