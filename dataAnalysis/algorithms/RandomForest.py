from sklearn.ensemble import RandomForestClassifier
from dataAnalysis.algorithms.Model import Model


class RandomForest(Model):
    def __init__(self, training_data, validation_data):
        ntrees = 495
        maxSplits = 79
        learn_rate = 0.90369
        random_forest = RandomForestClassifier(n_estimators=ntrees, max_leaf_nodes=maxSplits, n_jobs=-1)
        super().__init__(training_data=training_data,validation_data=validation_data, model=random_forest)
