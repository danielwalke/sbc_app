from imblearn.ensemble import RUSBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from dataAnalysis.algorithms.Model import Model


class RusBoostClassifier(Model):
    def __init__(self, training_data, validation_data):
        ntrees = 495
        maxSplits = 79
        learn_rate = 0.90369
        #sampling_strategy='not majority'
        rus_boost = RUSBoostClassifier(base_estimator=DecisionTreeClassifier(max_leaf_nodes=maxSplits),
                                       learning_rate=learn_rate, n_estimators=ntrees,
                                       random_state=1714400672, replacement=True)

        super().__init__(training_data=training_data,validation_data=validation_data, model=rus_boost)
