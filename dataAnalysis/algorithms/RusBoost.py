from imblearn.ensemble import RUSBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from dataAnalysis.algorithms.Model import Model


class RusBoostClassifier(Model):
    def __init__(self, training_data, validation_data):
        rus_boost = RUSBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=700, max_leaf_nodes=40),
                                       sampling_strategy='not majority')
        super().__init__(training_data=training_data,validation_data=validation_data, model=rus_boost)
