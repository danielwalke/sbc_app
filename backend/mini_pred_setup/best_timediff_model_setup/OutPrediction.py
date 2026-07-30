from pydantic import BaseModel
from typing import Union
from typing import Optional

class OutPrediction(BaseModel):
    predictions: list = []
    pred_probas: list = []
    classifier: str = None
    auroc: Optional[float] = None

    def __init__(self):
        super().__init__()
        self.predictions = []
        self.pred_probas = []
        self.auroc = None
        self.classifier = None

    def set_predictions(self, predictions):
        self.predictions = predictions

    def set_pred_probas(self, pred_probas):
        self.pred_probas = pred_probas

    def set_auroc(self, auroc):
        self.auroc = auroc

    def set_classifier(self, clf):
        self.classifier = clf

    def __str__(self):
        return f"""
        Predictions: {self.predictions}\n
        Pred proba: {self.pred_probas}\n
        """
