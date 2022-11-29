from dataAnalysis.Age import Age
from dataAnalysis.Diagnosis import Diagnosis
from dataAnalysis.Sex import Sex
from dataAnalysis.Center import Center
from dataAnalysis.Set import Set
from dataAnalysis.WBC import WBC
from dataAnalysis.TargetIcu import TargetIcu
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from dataAnalysis.learning.Training import Training
from dataAnalysis.learning.Testing import Testing
from sklearn.metrics import roc_auc_score
from sklearn import svm


def count_cbc_cases(data):
    comp_data = data.query("~(WBC.isnull() & HGB.isnull() & MCV.isnull() & PLT.isnull() & RBC.isnull())", engine='python')
    unique_data = comp_data.drop_duplicates(subset=["Id", "Center"])
    return len(unique_data)


def count_cbc(data):
    comp_data = data.query("~(WBC.isnull() & HGB.isnull() & MCV.isnull() & PLT.isnull() & RBC.isnull())", engine='python')
    return len(comp_data)

class DataAnalysis:
    def __init__(self, data):
        leipzig_training_data = data.query("Center == 'Leipzig' & Set == 'Training'")
        unique_data = leipzig_training_data.drop_duplicates(subset=["Id", "Center", "Time"], keep=False)
        non_icu_unique_data = unique_data.query("~(Sender.str.contains('ICU'))", engine='python')
        first_non_icu_unique_data = non_icu_unique_data.query("Episode == 1 ", engine='python')
        complete_first_non_icu_unique_data = first_non_icu_unique_data.query("~(WBC.isnull() | HGB.isnull() | "
                                                                             "MCV.isnull() | PLT.isnull() | "
                                                                             "RBC.isnull())", engine='python')
        sirs_complete_first_non_icu_unique_data = complete_first_non_icu_unique_data.query("Diagnosis != 'SIRS'", engine='python')
        self.data = sirs_complete_first_non_icu_unique_data
        self.control_data = self.data.query("(Diagnosis == 'Control' | (SecToIcu > 6*3600 & "
                                            "(~TargetIcu.isnull() & TargetIcu.str.contains('MICU'))))", engine='python')
        self.sepsis_data = self.data.query("Diagnosis == 'Sepsis'", engine='python')
        self.sepsis_data = self.sepsis_data.query("(~TargetIcu.isnull() & TargetIcu.str.contains('MICU'))",
                                                  engine='python')
        self.sepsis_data = self.sepsis_data.query("SecToIcu <= 6*3600", engine='python')
        print(f"Control data are {count_cbc_cases(self.control_data)} cases "
              f"and {count_cbc(self.control_data)} CBCs")
        print(f"Control data are {count_cbc_cases(self.control_data)} cases "
              f"and {count_cbc(self.control_data)} CBCs")
        print(f"Sepsis data are {count_cbc_cases(self.sepsis_data)} cases "
              f"and {count_cbc(self.sepsis_data)} CBCs")
        self.age_analysis = Age(self.data)
        self.sex_analysis = Sex(self.data)
        self.diagnoses_analysis = Diagnosis(self.data)
        self.center_analysis = Center(self.data)
        self.set_analysis = Set(self.data)
        self.wbc_analysis = WBC(self.data)
        self.target_icus = TargetIcu(self.data)

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
        print(header)
        print(self.data.head())

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
        training = Training(self.data)
        testing = Testing(self.data)
        logistic_regression = LogisticRegression(max_iter=1000, random_state=0, solver="liblinear", penalty="l2")
        logistic_regression.fit(training.get_x(), training.get_y())
        score = logistic_regression.score(testing.get_x(), testing.get_y())
        print(score)
        auroc_train = roc_auc_score(training.get_y(), logistic_regression.predict_proba(training.get_x())[:, 1])
        auroc_test = roc_auc_score(testing.get_y(), logistic_regression.predict_proba(testing.get_x())[:, 1])
        print(auroc_train)
        print(auroc_test)

    def random_forest(self):
        training = Training(self.data)
        testing = Testing(self.data)
        random_forest = RandomForestClassifier()
        random_forest.fit(training.get_x(), training.get_y())
        score = random_forest.score(testing.get_x(), testing.get_y())
        print(score)
        auroc_train = roc_auc_score(training.get_y(), random_forest.predict_proba(training.get_x())[:, 1])
        auroc_test = roc_auc_score(testing.get_y(), random_forest.predict_proba(testing.get_x())[:, 1])
        print(auroc_train)
        print(auroc_test)

    # def rus_boost(self):
    #     training = Training(self.data)
    #     testing = Testing(self.data)
    #     rus_boost = RUSBoostClassifier()
    #     rus_boost.fit(training.get_x(), training.get_y())
    #     score = rus_boost.score(testing.get_x(), testing.get_y())
    #     print(score)
    #     auroc_train = roc_auc_score(training.get_y(), rus_boost.predict_proba(training.get_x())[:, 1])
    #     auroc_test = roc_auc_score(testing.get_y(), rus_boost.predict_proba(testing.get_x())[:, 1])
    #     print(auroc_train)
    #     print(auroc_test)

    def support_vector_machine(self):
        training = Training(self.data)
        testing = Testing(self.data)
        support_vector_machine = svm.SVC()
        support_vector_machine.fit(training.get_x(), training.get_y())
        score = support_vector_machine.score(testing.get_x(), testing.get_y())
        print(score)
        auroc_train = roc_auc_score(training.get_y(), support_vector_machine.predict_proba(training.get_x())[:, 1])
        auroc_test = roc_auc_score(testing.get_y(), support_vector_machine.predict_proba(testing.get_x())[:, 1])
