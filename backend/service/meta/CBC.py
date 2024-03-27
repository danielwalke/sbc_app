from pydantic import BaseModel
from typing import Union

class CBC(BaseModel):
    age: float
    sex: str
    HGB: float
    RBC: float
    WBC: float
    MCV: float
    PLT: float
    ground_truth: Union[None, int]
