from service.meta.OutGraphDetailsPredictions import OutGraphDetailsPredictions
from service.impl.GraphPrediction import GraphPrediction
import torch
import numpy as np

class GraphPredictionDetails(GraphPrediction):
    def __init__(self, cbc_items, model, thresholds, shap_explainer, standard_scaler):
        super().__init__(cbc_items, model, thresholds, standard_scaler)
        self.shap_explainer = shap_explainer

    def get_shapley_values(self):
        features_origin,features_time  = self.get_features_list()
        features= torch.cat([features_origin, features_time], dim = -1).cpu().numpy()
        explainer = self.shap_explainer
        if self.standard_scaler is not None:
            features = self.standard_scaler.transform(features)
        shap_values = explainer.shap_values(features)
        shap_values = np.array(shap_values)
        print(shap_values.shape)
        shap_values = shap_values.squeeze()
        shap_contains_probas_of_both_classes = shap_values.ndim == 1
        shap_values = shap_values if shap_contains_probas_of_both_classes else shap_values[-1, :]
        print(shap_values.shape)
        time_split = shap_values.shape[-1] // 2

        shap_dict = dict()

        shap_dict["original"] = shap_values[:time_split] if shap_values.ndim == 1 else shap_values[:, :time_split]
        shap_dict["time"] = shap_values[time_split:] if shap_values.ndim == 1 else shap_values[:, time_split:]
        shap_dict["combined"] = np.sum([shap_dict["original"], shap_dict["time"]], axis=0).tolist()
        shap_dict["original"] = shap_dict["original"].tolist()
        shap_dict["time"] = shap_dict["time"].tolist()

        return shap_dict

    def get_detailed_output(self):
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

    def get_detailed_prospective_output(self):
        self.construct_directed_graph()
        return self.get_detailed_output()

    def get_detailed_retrospective_output(self):
        self.construct_reversed_directed_graph()
        return self.get_detailed_output()