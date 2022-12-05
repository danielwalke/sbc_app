from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

class CrossValidation:
    def __int__(self,training_data, model):
        self.data = training_data
        self.model = model
        self.cross_validation = StratifiedKFold(n_splits=10, shuffle=True, random_state=1714400672)
        self.over_sampler = RandomOverSampler(random_state=42)

    def cross_validate(self):
        for i, (train, test) in enumerate(self.cross_validation.split(self.data.get_x(), self.data.get_y())):
            x_train_ros, y_train_ros = self.over_sampler.fit_resample(self.data.get_x()[train], self.data.get_y()[train])
            self.model.fit(x_train_ros, y_train_ros)
            score = self.model.score(self.data.get_x()[test], self.data.get_y()[test])
            print(f"Score of {i} is " + str(score))
            auroc_train = roc_auc_score(self.data[train].get_y(),
                                        self.model.predict_proba(self.data[train].get_x())[:, 1])
            auroc_test = roc_auc_score(self.data[test].get_y(),
                                       self.model.predict_proba(self.data[test].get_x())[:, 1])
            print(f"The AUROC for {i} training data is " + str(auroc_train))
            print(f"The AUROC for {i} testing data is " + str(auroc_test))