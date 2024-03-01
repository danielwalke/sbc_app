from pydantic import BaseModel
from typing import Union


class OutPrediction(BaseModel):
    predictions: list = []
    pred_probas: list = []

    def __init__(self):
        super().__init__()
        self.predictions = []
        self.pred_probas = []

    def set_predictions(self, predictions):
        self.predictions = predictions

    def set_pred_probas(self, pred_probas):
        self.pred_probas = pred_probas

    def __str__(self):
        return f"""
        Predictions: {self.predictions}\n
        Pred proba: {self.pred_probas}\n
        """
