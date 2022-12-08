from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

from dataAnalysis.algorithms.Model import Model


class BaggingEnsembleClassifier(Model):
    def __init__(self, training_data, validation_data):
        base_estimator = DecisionTreeClassifier()
        bagging_classifier = BaggingClassifier(base_estimator=base_estimator, n_estimators=700, random_state=42)
        super().__init__(training_data=training_data, validation_data=validation_data, model=bagging_classifier)
