
from sklearn.tree import DecisionTreeClassifier

from dataAnalysis.algorithms.Model import Model


class DecisionTree(Model):
    def __init__(self, training_data, validation_data):
        decision_tree = DecisionTreeClassifier(max_depth=12)
        super().__init__(training_data=training_data,validation_data=validation_data, model=decision_tree)
