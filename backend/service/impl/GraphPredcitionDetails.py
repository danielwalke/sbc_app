from service.meta.OutGraphDetailsPredictions import OutGraphDetailsPredictions
from service.impl.GraphPrediction import GraphPrediction


class GraphPredictionDetails(GraphPrediction):
    def __init__(self, cbc_items, models, thresholds, shap_explainers):
        super().__init__(cbc_items, models, thresholds)
        self.shap_explainers = shap_explainers
        if len(self.shap_explainers) < 2:
            raise Exception("Missing shap explainers for GraphAware")

    def get_shapley_values(self):
        X_0, X_3 = self.get_features_list()
        explainer_0 = self.shap_explainers[0]
        shap_values_0 = explainer_0.shap_values(X_0.cpu().numpy())

        explainer_3 = self.shap_explainers[1]
        shap_values_3 = explainer_3.shap_values(X_3.cpu().numpy())

        shap_dict = dict()
        shap_dict["combined"] = (shap_values_0[1] + shap_values_3[1]).tolist()
        shap_dict["original"] = shap_values_0[1].tolist()
        shap_dict["time"] = shap_values_3[1].tolist()

        return shap_dict

    def get_detailed_output(self):
        self.construct_graph()
        self.set_pred_proba()
        output = OutGraphDetailsPredictions()
        print("Start classification")
        print(self.get_pred_proba().tolist())
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        print("Finished classification")
        print("Started Shapley values calculation")
        output.set_shap_values_list(self.get_shapley_values())
        print("Finished Shapley values calculation")
        return output
