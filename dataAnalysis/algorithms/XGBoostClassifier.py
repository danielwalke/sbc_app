import xgboost as xgb

from dataAnalysis.algorithms.Model import Model



class XGBoostClassifier(Model):
    def __init__(self, training_data, validation_data, greifswald_validation):
        ntrees = 495
        maxSplits = 79
        learn_rate = 0.90369
        xg_boost = xgb.XGBClassifier()
        super().__init__(training_data=training_data,validation_data=validation_data,greifswald_validation=greifswald_validation, model=xg_boost)
