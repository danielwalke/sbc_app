from service.impl.PredictionDetails import PredictionDetails
from service.meta.OutDetailsPrediction import OutDetailsPrediction
from service.meta.OutDetailsPredictions import OutDetailsPredictions
import shap


class DetailsPrediction:

    def __init__(self, cbc_items, models, thresholds, background_data):
        self.cbc_items = cbc_items
        self.models = models
        self.out_details_predictions = OutDetailsPredictions()
        self.thresholds = thresholds
        self.background_data = background_data

    def get_output(self):
        for i, model in enumerate(self.models):
            shap_explainer = shap.LinearExplainer(model, self.background_data) \
                if model.__class__.__name__ == "LogisticRegression" else shap.TreeExplainer(model)
            prediction = PredictionDetails([self.cbc_items[i]], model,self.thresholds, shap_explainer)
            out_details_prediction: OutDetailsPrediction = prediction.get_detailed_output()
            out_details_prediction.set_classifier_name(model.__class__.__name__)
            self.out_details_predictions.add_prediction_detail(out_details_prediction)
        return self.out_details_predictions
