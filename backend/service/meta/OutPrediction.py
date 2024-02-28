from pydantic import BaseModel
from typing import Union


class OutPrediction(BaseModel):
    predictions: list = []
    pred_probas: list = []
    shap_values: list = []

    def __init__(self):
        super().__init__()
        self.predictions = []
        self.pred_probas = []
        self.shap_values = []

    def set_predictions(self, predictions):
        self.predictions = predictions

    def set_pred_probas(self, pred_probas):
        self.pred_probas = pred_probas

    def set_shap_values(self, shap_values):
        self.shap_values = shap_values

    def __str__(self):
        return f"""
        Predictions: {self.predictions}\n
        Pred proba: {self.pred_probas}\n
        Shap values: {self.shap_values}\n
        """
