from service.impl.GraphPredictionDetails import GraphPredictionDetails
from service.meta.OutGraphDetailsPredictions import OutGraphDetailsPredictions
from service.meta.OutDetailsPredictions import OutDetailsPredictions
import shap


class DetailsPredictionGraph:

    def __init__(self, graph_cbc_items, model, explainer, threshold):
        self.graph_cbc_items = graph_cbc_items
        self.model = model
        self.explainer = explainer
        self.threshold = threshold

        self.out_details_predictions = OutDetailsPredictions()


    def get_prospective_output(self):
        print(f"Start prediction for prospective analysis")
        prediction = GraphPredictionDetails(self.graph_cbc_items, self.model, self.threshold, self.explainer)
        out_details_prediction: OutGraphDetailsPredictions = prediction.get_detailed_prospective_output()
        out_details_prediction.set_classifier_name(f"prospective_{self.model.__class__.__name__}")
        self.out_details_predictions.set_prediction_detail(out_details_prediction)
        return self.out_details_predictions

    def get_retrospective_output(self):
        print(f"Start prediction for retrospective analysis")
        prediction = GraphPredictionDetails(self.graph_cbc_items, self.model, self.threshold, self.explainer)
        out_details_prediction: OutGraphDetailsPredictions = prediction.get_detailed_retrospective_output()
        out_details_prediction.set_classifier_name(f"retrospective_{self.model.__class__.__name__}")
        self.out_details_predictions.set_prediction_detail(out_details_prediction)
        return self.out_details_predictions