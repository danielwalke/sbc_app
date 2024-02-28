from service.impl.Prediction import Prediction
from service.meta.OutDetailsPrediction import OutDetailsPrediction
from service.meta.OutDetailsPredictions import OutDetailsPredictions
from service.meta.OutPrediction import OutPrediction
import shap


class DetailsPrediction:

    def __init__(self, cbc_items, models):
        self.cbc_items = cbc_items
        self.models = models
        self.out_details_predictions = OutDetailsPredictions()

    def get_output(self):
        for model in self.models:
            print(f"Start prediction for {model.__class__.__name__}")
            shap_explainer = shap.LinearExplainer if model.__class__.__name__ == "Logistic Regression" else shap.TreeExplainer
            prediction = Prediction(self.cbc_items, model, shap_explainer)
            out_predictions: OutPrediction = prediction.get_output()
            out_details_prediction = OutDetailsPrediction()
            out_details_prediction.set_prediction(out_predictions.predictions[-1])
            out_details_prediction.set_shap_values(out_predictions.pred_probas[-1])
            out_details_prediction.set_pred_proba(out_predictions.shap_values[-1])
            out_details_prediction.set_classifier_name(model.__class__.__name__)
            self.out_details_predictions.add_prediction_detail(out_details_prediction)
        return self.out_details_predictions
