import numpy as np
import shap
from service.meta.OutPrediction import OutPrediction


class Prediction:
    def __init__(self, cbc_items, model):
        self.cbc_items = cbc_items
        self.model = model

    def get_features(self):
        X = np.zeros((len(self.cbc_items), 7))

        for i, cbc_item in enumerate(self.cbc_items):
            categorical_sex = 1 if cbc_item.sex == "W" else 0
            cbc_array = [cbc_item.age, categorical_sex, cbc_item.HGB, cbc_item.WBC, cbc_item.RBC, cbc_item.MCV,
                         cbc_item.PLT]
            X[i, :] = cbc_array
        return X

    def get_pred_proba(self):
        X = self.get_features()
        return self.model.predict_proba(X)[:, 1]

    def get_prediction(self):
        return self.get_pred_proba() >= 0.3547

    def get_shapley_values(self):
        X = self.get_features()
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        return shap_values[1]

    def get_output(self):
        output = OutPrediction()
        print("Start classification")
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        print("Finished classification")
        print("Started Shapley values calculation")
        output.set_shap_values(self.get_shapley_values().tolist())
        print("Finished Shapley values calculation")
        return output
