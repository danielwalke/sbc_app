
from sklearn.neighbors import KNeighborsClassifier

from dataAnalysis.algorithms.Model import Model


class KNeighbors(Model):
    def __init__(self, training_data, validation_data):
        k_neighbors = KNeighborsClassifier()
        super().__init__(training_data=training_data,validation_data=validation_data, model=k_neighbors)
