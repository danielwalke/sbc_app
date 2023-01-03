from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from statistics import mean
from sklearn import metrics
import matplotlib.pyplot as plt

class Model:
    def __init__(self, training_data, validation_data,greifswald_validation, model):
        self.training_data = training_data
        self.validation_data = validation_data
        self.greifswald_validation = greifswald_validation
        self.model = model
        self.cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=1714400672)

    def cross_validate(self):
        train_auroc = []
        test_auroc = []
        val_auroc = []
        # for i, (train, test) in enumerate(
        #         self.cross_validation.split(self.training_data.get_x(), self.training_data.get_y())):
        #     ros = RandomOverSampler(random_state=42)
        #     x_data_train = self.training_data.get_x().filter(items=train, axis=0)
        #     x_data_test = self.training_data.get_x().filter(items=test, axis=0)
        #     y_data_train = self.training_data.get_y().filter(items=train, axis=0)
        #     y_data_test = self.training_data.get_y().filter(items=test, axis=0)
        #
        #     # x_train_ros, y_train_ros = ros.fit_resample(x_data_train, y_data_train)
        #     self.model.fit(x_data_train, y_data_train)
        #     score = self.model.score(x_data_test, y_data_test)
        #     # print(f"Score of {i} is " + str(score))
        #     auroc_train = roc_auc_score(y_data_train,
        #                                 self.model.predict_proba(x_data_train)[:, 1])
        #     auroc_test = roc_auc_score(y_data_test,
        #                                self.model.predict_proba(x_data_test)[:, 1])
        #     auroc_val = roc_auc_score(self.validation_data.get_y(),
        #                               self.model.predict_proba(self.validation_data.get_x())[:, 1])
        #     train_auroc.append(auroc_train)
        #     test_auroc.append(auroc_test)
        #     val_auroc.append(auroc_val)
        #     print(f"The AUROC for {i} training data is " + str(auroc_train))
        #     print(f"The AUROC for {i} testing data is " + str(auroc_test))
        #     print(f"The AUROC for {i} validation data is " + str(auroc_val))

        ros = RandomOverSampler(random_state=42)

        x_data_train = self.training_data.get_x()
        y_data_train = self.training_data.get_y()

        # x_train_ros, y_train_ros = ros.fit_resample(x_data_train, y_data_train)
        self.model.fit(x_data_train, y_data_train)

        auroc_train = roc_auc_score(y_data_train,
                                    self.model.predict_proba(x_data_train)[:, 1])
        auroc_val = roc_auc_score(self.validation_data.get_y(),
                                  self.model.predict_proba(self.validation_data.get_x())[:, 1])
        auroc_val_gw = roc_auc_score(self.greifswald_validation.get_y(),
                                  self.model.predict_proba(self.greifswald_validation.get_x())[:, 1])
        print(f"The AUROC for training data is " + str(auroc_train))
        print(f"The AUROC for validation data is " + str(auroc_val))
        print(f"The AUROC for greifswald validation data is " + str(auroc_val_gw))

        print(len(self.validation_data.get_y()))
        print(self.validation_data.get_y().shape)
        confusion_matrix = metrics.confusion_matrix(self.validation_data.get_y(),
                                                    self.model.predict(self.validation_data.get_x()))

        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[False, True])

        cm_display.plot()
        plt.show()

        return self.model
        # print(f"The mean AUROC for training data is " + str(mean(train_auroc)))
        # print(f"The mean AUROC for testing data is " + str(mean(test_auroc)))
        # print(f"The mean AUROC for validation data is " + str(mean(val_auroc)))
        ## TODO Confusion matrix
