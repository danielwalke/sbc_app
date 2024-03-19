from pydantic import BaseModel


class CBC(BaseModel):
    age: float
    sex: str
    HGB: float
    RBC: float
    WBC: float
    MCV: float
    PLT: float
    ground_truth: bool
