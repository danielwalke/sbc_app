from pydantic import BaseModel
from service.meta.CBC import CBC


class InPredictionDetails(BaseModel):
    data: CBC
    classifier: str