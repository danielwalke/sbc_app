from sklearn.ensemble import ExtraTreesClassifier
from dataAnalysis.algorithms.Model import Model


class ExtraTrees(Model):
    def __init__(self, training_data, validation_data):
        extra_trees = ExtraTreesClassifier(n_estimators=700, max_leaf_nodes=40)
        super().__init__(training_data=training_data,validation_data=validation_data, model=extra_trees)
