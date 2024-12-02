import numpy as np
import shap
from sklearn.metrics import roc_auc_score

from service.meta.OutPrediction import OutPrediction
from service.meta.CBC import CBC
import time

class Prediction:
    def __init__(self, cbc_items, model, threshold):
        self.cbc_items:CBC = cbc_items
        self.model = model
        self.threshold = threshold

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
        return self.get_pred_proba() >= self.threshold

    def get_auroc(self):
        y = list(map(lambda cbc_item: cbc_item.ground_truth, self.cbc_items))
        if not np.isnan(y).any() and np.unique(y).shape[0] == 2:
            print(roc_auc_score(y, self.get_pred_proba()))
        return None if np.unique(y).shape[0] != 2 else roc_auc_score(y, self.get_pred_proba())

    def get_output(self):
        output = OutPrediction()
        output.set_classifier(self.model.__class__.__name__)
        print("Start classification")
        start = time.time()
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        try:
            output.set_auroc(self.get_auroc())
        except:
            print("Couldnt calculate auroc")
        print(f"Required Classification time: {time.time() - start} s")
        print("Finished classification")
        return output
