from pydantic import BaseModel
from service.meta.GraphCBC import GraphCBC


class InGraphPrediction(BaseModel):
    data: list[GraphCBC]
    classifier: str
