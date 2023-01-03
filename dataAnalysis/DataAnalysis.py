import math

from imblearn.over_sampling import RandomOverSampler
from sklearn.tree import DecisionTreeClassifier

from dataAnalysis.patientData.bloodValues.WBC import WBC
from dataAnalysis.patientData.bloodValues.HGB import HGB
from dataAnalysis.patientData.bloodValues.CRP import CRP
from dataAnalysis.patientData.bloodValues.MCV import MCV
from dataAnalysis.patientData.bloodValues.RBC import RBC
from dataAnalysis.patientData.bloodValues.PLT import PLT
from dataAnalysis.patientData.bloodValues.PCT import PCT
from dataAnalysis.algorithms.LogisticRegression import LogisticRegressionClassifier
from dataAnalysis.algorithms.RusBoost import RusBoostClassifier
from dataAnalysis.algorithms.RandomForest import RandomForest
from dataAnalysis.algorithms.BaggingEnsembleClassifier import BaggingEnsembleClassifier
from dataAnalysis.algorithms.ExtraTrees import ExtraTrees
from dataAnalysis.algorithms.KNeighbors import KNeighbors
from dataAnalysis.algorithms.DecisionTree import DecisionTree
from dataAnalysis.data.Training import Training
from dataAnalysis.data.Features import Features
from dataAnalysis.data.Validation import Validation
from sklearn.metrics import roc_auc_score
from sklearn import svm
from lazypredict.Supervised import LazyClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from dialnd_imbalanced_algorithms.imbalanced_algorithms.rus import RUSBoost
from dialnd_imbalanced_algorithms.imbalanced_algorithms.smote import SMOTEBoost
import pandas as pd
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn import metrics

def count_cbc_cases(data):
    comp_data = data.query("~(WBC.isnull() & HGB.isnull() & MCV.isnull() & PLT.isnull() & RBC.isnull())",
                           engine='python')
    unique_data = comp_data.drop_duplicates(subset=["Id", "Center"])
    return len(unique_data)


def count_cbc(data):
    comp_data = data.query("~(WBC.isnull() & HGB.isnull() & MCV.isnull() & PLT.isnull() & RBC.isnull())",
                           engine='python')
    return len(comp_data)


# TODO Completely re-egineer their model for reproducability or searching through all algorithms to find
#  a better one directly
class DataAnalysis:
    def __init__(self, data):
        self.training = Training(data)
        print("Training: ")
        print(f"Assessable data are {count_cbc_cases(self.training.get_data())} cases "
              f"and {count_cbc(self.training.get_data())} CBCs")
        print(f"Control data are {count_cbc_cases(self.training.get_control_data())} cases "
              f"and {count_cbc(self.training.get_control_data())} CBCs")
        print(f"Sepsis data are {count_cbc_cases(self.training.get_sepsis_data())} cases "
              f"and {count_cbc(self.training.get_sepsis_data())} CBCs")
        print(20 * "$")
        print("Testing: ")
        self.validation = Validation(data)
        print(f"Controls: {self.validation.get_control_data().shape[0]},"
              f" Sepsis: {self.validation.get_sepsis_data().shape[0]}")
        print(f"Assessable data are {count_cbc_cases(self.validation.get_data())} cases "
              f"and {count_cbc(self.validation.get_data())} CBCs")
        print(f"Control data are {count_cbc_cases(self.validation.get_control_data())} cases "
              f"and {count_cbc(self.validation.get_control_data())} CBCs")
        print(f"Sepsis data are {count_cbc_cases(self.validation.get_sepsis_data())} cases "
              f"and {count_cbc(self.validation.get_sepsis_data())} CBCs")
        # self.training.get_data().to_csv("leipzig_training.csv")
        # self.validation.get_data().to_csv("leipzig_validation.csv")
        # self.age_analysis = Age(self.data)
        # self.sex_analysis = Sex(self.data)
        # self.diagnoses_analysis = Diagnosis(self.data)
        # self.center_analysis = Center(self.data)
        # self.set_analysis = Set(self.data)

        # self.wbc_analysis = WBC(self.training.get_data())
        # self.wbc_analysis.violin_plot()
        # self.hgb_analysis = HGB(self.training.get_data())
        # self.hgb_analysis.violin_plot()
        # self.mcv_analysis = MCV(self.training.get_data())
        # self.mcv_analysis.violin_plot()
        # self.plt_analysis = PLT(self.training.get_data())
        # self.plt_analysis.violin_plot()
        # self.rbc_analysis = RBC(self.training.get_data())
        # self.rbc_analysis.violin_plot()
        # self.crp_analysis = CRP(self.training.get_data())
        # self.crp_analysis.violin_plot()
        # self.pct_analysis = PCT(self.training.get_data())
        # self.pct_analysis.violin_plot()

        self.cross_validation = KFold(n_splits=10, random_state=1714400672, shuffle=True)
        # self.target_icus = TargetIcu(self.data)

    def lazy_predict(self):
        classifier = LazyClassifier(verbose=2, ignore_warnings=True, custom_metric=None)
        ros = RandomOverSampler(random_state=42)
        x_train_ros, y_train_ros = ros.fit_resample(self.training.get_x(), self.training.get_y())
        x_train, x_test, y_train, y_test = train_test_split(x_train_ros, y_train_ros,
                                                            test_size=0.33, random_state=42)
        models, predictions = classifier.fit(x_train, x_test, y_train, y_test)
        print(models)

    def show_text_information(self):
        self.age_analysis.get_avg_age()
        median_age = self.age_analysis.get_media_age()
        header = self.data.columns.values.tolist()
        print(20 * "#")
        print(f"The median age is {round(median_age, 1)}")
        print(f"The average age is {round(self.age_analysis.get_avg_age(), 1)}")
        print(20 * "#")
        print(len(self.data))
        print(f"Number of sepsis cases {self.diagnoses_analysis.get_numer_of_cases()}")
        print(f"Number of sirs cases {self.diagnoses_analysis.get_numer_of_sirs()}")
        print(f"Number of control cases {self.diagnoses_analysis.get_number_of_controls()}")
        print(20 * "#")
        print(f"The median number of white blood cells is {round(self.wbc_analysis.get_median_wbc(), 1)}")
        print(f"The average number of white blood cells is {round(self.wbc_analysis.get_average_wbc(), 1)}")

    def show_diagrams(self):
        self.age_analysis.visualize_age()
        self.sex_analysis.visualize_sex()
        self.diagnoses_analysis.visualize_diagnoses()
        self.center_analysis.visualize_diagnoses()
        self.set_analysis.visualize_sets()

    def show_comparison_diagrams(self):
        self.age_analysis.compare_ages()
        self.wbc_analysis.visualize_wbc_comparison()

    def logistic_regression(self):
        logistic_regression = LogisticRegressionClassifier(training_data=self.training, validation_data=self.validation)
        logistic_regression.cross_validate()

    def random_forest(self):
        print("Execute random forest")
        random_forest = RandomForest(training_data=self.training, validation_data=self.validation)
        random_forest.cross_validate()

    def bagging_classifier(self):
        print("Execute bagging classifier")
        bagging_classifier = BaggingEnsembleClassifier(training_data=self.training, validation_data=self.validation)
        bagging_classifier.cross_validate()

    def extra_trees(self):
        print("Execute extra trees classifier")
        extra_trees = ExtraTrees(training_data=self.training, validation_data=self.validation)
        extra_trees.cross_validate()

    def k_neighbors(self):
        print("Execute k-nearest neighbors classifier")
        k_neighbors = KNeighbors(training_data=self.training, validation_data=self.validation)
        k_neighbors.cross_validate()

    def rus_boost(self):
        print("Execute RUS Boost")
        rus_boost = RusBoostClassifier(training_data=self.training, validation_data=self.validation)
        rus_boost.cross_validate()

    def decision_tree(self):
        print("Execute Decision Tree")
        rus_boost = DecisionTree(training_data=self.training, validation_data=self.validation)
        trained_model = rus_boost.cross_validate()
        features = pd.DataFrame(trained_model.feature_importances_, index=self.validation.get_x().columns)
        print(features)

    def support_vector_machine(self):
        support_vector_machine = svm.SVC()
        support_vector_machine.fit(self.training.get_x(), self.training.get_y())
        score = support_vector_machine.score(self.validation.get_x(), self.validation.get_y())
        print(f"Score is " + str(score))
        auroc_train = roc_auc_score(self.training.get_y(),
                                    support_vector_machine.predict_proba(self.training.get_x())[:, 1])
        auroc_test = roc_auc_score(self.validation.get_y(),
                                   support_vector_machine.predict_proba(self.validation.get_x())[:, 1])
        print(f"The AUROC for training data is " + str(auroc_train))
        print(f"The AUROC for testing data is " + str(auroc_test))

    def dialnd_rus_boost(self):
        target_names = self.validation.get_y().unique()
        print(target_names)
        # ntrees = 100
        # maxSplits = 300
        # learn_rate = 0.90369 #65:35 #auroc:  0.854
        ntrees = 500
        maxSplits = 500
        learn_rate = 0.50369
        undersampling_factor = 0.65
        sample_disbalance = math.floor((len(self.training.get_y()[self.training.get_y() == 'Control']) - len(
            self.training.get_y()[self.training.get_y() == 'Sepsis'])) * undersampling_factor)
        sample_disbalance = len(self.training.get_y()[self.training.get_y() == 'Control']) - math.floor(len(
            self.training.get_y()[self.training.get_y() == 'Sepsis'])*65/35)
        print(sample_disbalance)
        print(len(
            self.training.get_y()[self.training.get_y() == 'Sepsis']))
        print(len(
            self.training.get_y()[self.training.get_y() == 'Control']))
        ## SMOTEBoost(n_estimators=ntrees, base_estimator=DecisionTreeClassifier(max_leaf_nodes=maxSplits),
                                    ## n_samples=sample_disbalance, learning_rate=learn_rate),
        for algorithm in [RUSBoost(n_samples=sample_disbalance,
                                   base_estimator=DecisionTreeClassifier(max_leaf_nodes=maxSplits),
                                   learning_rate=learn_rate, n_estimators=ntrees,
                                   random_state=1714400672, with_replacement=False)]:
            algorithm.fit(self.training.get_x(), self.training.get_y())
            y_pred = algorithm.predict(self.validation.get_x())
            # print(str(algorithm))
            # print()
            confusion_matrix = metrics.confusion_matrix(self.validation.get_y(),
                                                        y_pred)

            cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[False, True])

            cm_display.plot()

            auroc_train = roc_auc_score(self.training.get_y(),
                                        algorithm.predict_proba(self.training.get_x())[:, 1])
            auroc_val = roc_auc_score(self.validation.get_y(),
                                      algorithm.predict_proba(self.validation.get_x())[:, 1])
            print(f"The AUROC for training data is " + str(auroc_train))
            print(f"The AUROC for validation data is " + str(auroc_val))
            print(classification_report(self.validation.get_y(), y_pred,
                                        target_names=target_names))

            plt.show()
