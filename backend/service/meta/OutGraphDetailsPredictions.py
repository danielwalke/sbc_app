from typing import Union


class OutGraphDetailsPredictions:
    predictions: list
    pred_probas: list
    shap_values_list: list
    classifier_name: Union[str, None]

    def __init__(self):
        super().__init__()
        self.predictions = []
        self.pred_probas = []
        self.shap_values = []
        self.classifier_name = None

    def set_predictions(self, predictions):
        self.predictions = predictions

    def set_pred_probas(self, pred_probas):
        self.pred_probas = pred_probas

    def set_shap_values_list(self, shap_values_list):
        self.shap_values_list = shap_values_list

    def set_classifier_name(self, classifier_name):
        self.classifier_name = classifier_name
