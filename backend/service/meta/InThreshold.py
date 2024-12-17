from pydantic import BaseModel
from typing import Optional


class InThreshold(BaseModel):
	min_sensitivity: Optional[float]
