import numpy as np
import shap
from service.meta.OutDetailsPrediction import OutDetailsPrediction
from service.impl.Prediction import Prediction


class PredictionDetails(Prediction):
    def __init__(self, cbc_items, model, thresholds, shap_explainer):
        super().__init__(cbc_items, model, thresholds)
        self.shap_explainer = shap_explainer

    def get_shapley_values(self):
        X = self.get_features()
        shap_values = self.shap_explainer.shap_values(X)
        return shap_values[1] if isinstance(shap_values, list) else shap_values

    def get_detailed_output(self):
        output = OutDetailsPrediction()
        print("Start classification")
        print(self.get_pred_proba().tolist())
        output.set_prediction(self.get_prediction().tolist()[-1])
        output.set_pred_proba(self.get_pred_proba().tolist()[-1])
        print("Finished classification")
        print("Started Shapley values calculation")
        output.set_shap_values(self.get_shapley_values().tolist()[-1])
        print(output)
        print("Finished Shapley values calculation")
        return output
