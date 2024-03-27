from service.impl.GraphPredcitionDetails import GraphPredictionDetails
from service.meta.OutGraphDetailsPredictions import OutGraphDetailsPredictions
from service.meta.OutDetailsPredictions import OutDetailsPredictions
import shap


class DetailsPredictionGraph:

    def __init__(self, graph_cbc_items, models, thresholds):
        self.graph_cbc_items = graph_cbc_items
        self.models = models
        self.out_details_predictions = OutDetailsPredictions()
        self.thresholds = thresholds

    def get_output(self):
        print(f"Start prediction for GraphAware")
        shap_explainers = (shap.TreeExplainer(self.models[0]), shap.TreeExplainer(self.models[1]))
        prediction = GraphPredictionDetails(self.graph_cbc_items, self.models, self.thresholds, shap_explainers)
        out_details_prediction: OutGraphDetailsPredictions = prediction.get_detailed_output()
        out_details_prediction.set_classifier_name("GraphAware")
        self.out_details_predictions.add_prediction_detail(out_details_prediction)
        return self.out_details_predictions
