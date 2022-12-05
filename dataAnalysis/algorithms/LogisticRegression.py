from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from dataAnalysis.algorithms.CrossValidation import CrossValidation


class LogisticRegressionClassifier(CrossValidation):
    def __init__(self, training_data):
        print(training_data)
        self.data = training_data
        self.logistic_regression = LogisticRegression(max_iter=1000, random_state=0, solver="liblinear", penalty="l2")
        super().__int__(training_data=training_data, model=self.logistic_regression)

    def cross_validate(self):
        for i, (train, test) in enumerate(self.cross_validation.split(self.data.get_x(), self.data.get_y())):
            ros = RandomOverSampler(random_state=42)
            x_data_train = self.data.get_x().filter(items=train, axis=0)
            x_data_test = self.data.get_x().filter(items=test, axis=0)
            y_data_train = self.data.get_y().filter(items=train, axis=0)
            y_data_test = self.data.get_y().filter(items=test, axis=0)
            print(x_data_train.head())
            print(len(x_data_train))
            print(len(x_data_test))

            x_train_ros, y_train_ros = ros.fit_resample(x_data_train, y_data_train)
            self.logistic_regression.fit(x_train_ros, y_train_ros)
            score = self.logistic_regression.score(x_data_test, y_data_test)
            print(f"Score of {i} is " + str(score))
            auroc_train = roc_auc_score(y_train_ros,
                                        self.logistic_regression.predict_proba(x_train_ros)[:, 1])
            auroc_test = roc_auc_score(y_data_test,
                                       self.logistic_regression.predict_proba(x_data_test)[:, 1])
            print(f"The AUROC for {i} training data is " + str(auroc_train))
            print(f"The AUROC for {i} testing data is " + str(auroc_test))
