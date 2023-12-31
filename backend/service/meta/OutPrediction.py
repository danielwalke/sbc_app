from pydantic import BaseModel


class OutPrediction(BaseModel):
    predictions:list = []
    pred_probas:list = []
    shap_values:list = []

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
