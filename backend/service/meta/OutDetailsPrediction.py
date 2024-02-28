from typing import Union


class OutDetailsPrediction:
    prediction: Union[bool, None]
    pred_proba: Union[float, None]
    shap_values: list
    classifier_name: Union[str, None]

    def __init__(self):
        super().__init__()
        self.prediction = None
        self.pred_proba = None
        self.shap_values = []
        self.classifier_name = None

    def set_prediction(self, prediction):
        self.prediction = prediction

    def set_pred_proba(self, pred_proba):
        self.pred_proba = pred_proba

    def set_shap_values(self, shap_values):
        self.shap_values = shap_values

    def set_classifier_name(self, classifier_name):
        self.classifier_name = classifier_name