import httpx
from pydantic import BaseModel
from typing import Optional
import asyncio

class CBC(BaseModel):
    age: float
    sex: str
    HGB: float
    WBC: float
    RBC: float
    MCV: float
    PLT: float
    ground_truth: Optional[int]

class InPrediction(BaseModel):
    data: list[CBC]
    classifier: str
    threshold: float

async def request_standard_pred(url: str, data, classifier: str, threshold: float):
    payload = InPrediction(data=data, classifier=classifier, threshold=threshold).dict()
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.json()

STANDARD_RF_THRESHOLD = 0.3098 ## Threshold is estimated based on Receiver Operating Curve
sample_data = [
	{"age": 18, "sex": 'W', "HGB": 9, "WBC": 4, "RBC": 5, "MCV": 80, "PLT": 500},
	{"age": 80, "sex": 'W', "HGB": 9, "WBC": 40, "RBC": 5, "MCV": 80, "PLT": 500},
]
result = asyncio.run(request_standard_pred("https://daniel-walke.com/sbc_backend/get_standard_pred", sample_data, "RandomForestClassifier", STANDARD_RF_THRESHOLD))
print(result)