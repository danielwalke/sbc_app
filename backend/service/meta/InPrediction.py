from pydantic import BaseModel
from service.meta.CBC import CBC


class InPrediction(BaseModel):
    data: list[CBC]
    classifier: str
    threshold: float