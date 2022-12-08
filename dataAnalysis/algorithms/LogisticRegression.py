from sklearn.linear_model import LogisticRegression
from dataAnalysis.algorithms.Model import Model


class LogisticRegressionClassifier(Model):
    def __init__(self, training_data, validation_data):
        logistic_regression = LogisticRegression(max_iter=1000, random_state=0, solver="liblinear", penalty="l2")
        super().__init__(training_data=training_data,validation_data=validation_data, model=logistic_regression)
