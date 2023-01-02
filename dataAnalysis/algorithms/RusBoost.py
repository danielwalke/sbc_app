from imblearn.ensemble import RUSBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from dataAnalysis.algorithms.Model import Model


class RusBoostClassifier(Model):
    def __init__(self, training_data, validation_data):
        ntrees = 495
        maxSplits = 79
        learn_rate = 0.90369
        rus_boost = RUSBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=ntrees, max_leaf_nodes=maxSplits),
                                       sampling_strategy='not majority', learning_rate=learn_rate,
                                       random_state=1714400672)

        super().__init__(training_data=training_data,validation_data=validation_data, model=rus_boost)
