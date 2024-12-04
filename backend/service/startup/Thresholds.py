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

    app.state.standard_thresholds = {
        "LogisticRegression": Thresholds.STANDARD_LR,
        "DecisionTreeClassifier": Thresholds.STANDARD_DT,
        "RandomForestClassifier": Thresholds.STANDARD_RF,
        "XGBClassifier": Thresholds.STANDARD_XGB,
        # "RUSBoostClassifier": Thresholds.STANDARD_RUS,
    }

    app.state.prospective_thresholds_ref_mean_diff = {
        "LogisticRegression": Thresholds.PROSPECTIVE_LR_MEAN_DIFF,
        "DecisionTreeClassifier": Thresholds.PROSPECTIVE_DT_MEAN_DIFF,
        "RandomForestClassifier": Thresholds.PROSPECTIVE_RF_MEAN_DIFF,
        "XGBClassifier": Thresholds.PROSPECTIVE_XGB_MEAN_DIFF,
    }