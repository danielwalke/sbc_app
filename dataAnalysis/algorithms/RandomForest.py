from sklearn.ensemble import RandomForestClassifier
from dataAnalysis.algorithms.Model import Model


class RandomForest(Model):
    def __init__(self, training_data, validation_data):
        random_forest = RandomForestClassifier()
        super().__init__(training_data=training_data,validation_data=validation_data, model=random_forest)
