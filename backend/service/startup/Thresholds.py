from service.constants import Thresholds


def initialize_thresholds(app):
    app.state.retrospective_thresholds = {
        "LogisticRegression": Thresholds.RETROSPECTIVE_LR,
        "DecisionTreeClassifier": Thresholds.RETROSPECTIVE_DT,
        "RandomForestClassifier": Thresholds.RETROSPECTIVE_RF,
        "XGBClassifier": Thresholds.RETROSPECTIVE_XGB,
    }
    app.state.prospective_thresholds = {
        "LogisticRegression": Thresholds.PROSPECTIVE_LR,
        "DecisionTreeClassifier": Thresholds.PROSPECTIVE_DT,
        "RandomForestClassifier": Thresholds.PROSPECTIVE_RF,
        "XGBClassifier": Thresholds.PROSPECTIVE_XGB,
    }