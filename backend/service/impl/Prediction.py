import numpy as np
import shap
from service.meta.OutPrediction import OutPrediction
import time
from sklearn.metrics import roc_auc_score

class Prediction:
    def __init__(self, cbc_items, model, thresholds):
        self.cbc_items = cbc_items
        self.model = model
        self.thresholds = thresholds

    def get_features(self):
        X = np.zeros((len(self.cbc_items), 7))
        for i, cbc_item in enumerate(self.cbc_items):
            categorical_sex = 1 if cbc_item.sex == "W" else 0
            cbc_array = [cbc_item.age, categorical_sex, cbc_item.HGB, cbc_item.WBC, cbc_item.RBC, cbc_item.MCV,
                         cbc_item.PLT]
            X[i, :] = cbc_array
        return X

    def get_labels(self):
        y = np.zeros((len(self.cbc_items), 1))
        for i, cbc_item in enumerate(self.cbc_items):
            y[i, 0] = cbc_item.ground_truth
        return y.astype(np.int8)

    def get_pred_proba(self):
        X = self.get_features()
        return self.model.predict_proba(X)[:, 1]

    def get_prediction(self):
        return self.get_pred_proba() >= self.thresholds[self.model.__class__.__name__]

    def get_auroc(self):
        y = self.get_labels()
        pred_proba = self.get_pred_proba()
        return roc_auc_score(y, pred_proba)

    def get_output(self):
        output = OutPrediction()
        print("Start classification")
        start = time.time()
        output.set_predictions(self.get_prediction().tolist())
        output.set_pred_probas(self.get_pred_proba().tolist())
        print(f"Required Classification time: {time.time() - start} s")
        print("Finished classification")
        print(f"AUROC: {self.get_auroc()}")
        return output
