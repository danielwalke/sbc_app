from joblib import load


def initialize_models(app):
    app.state.prospective_models = {
        "LogisticRegression": load('./models/prospective/prospective_logistic_regression.joblib'),
        "DecisionTreeClassifier": load('./models/prospective/prospective_decision_tree.joblib'),
        "XGBClassifier": load('./models/prospective/prospective_xgb.joblib'),
        "RandomForestClassifier": load('./models/prospective/prospective_random_forest.joblib'),
    }

    app.state.retrospective_models = {
        "LogisticRegression": load('./models/retrospective/retrospective_logistic_regression.joblib'),
        "DecisionTreeClassifier": load('./models/retrospective/retrospective_decision_tree.joblib'),
        "XGBClassifier": load('./models/retrospective/retrospective_xgb.joblib'),
        "RandomForestClassifier": load('./models/retrospective/retrospective_random_forest.joblib'),
    }

    app.state.prospective_ref_models = {
        "LogisticRegression": load('./models/prospectiveReference/prospective_logistic_regression_mean_diff.joblib'),
        "DecisionTreeClassifier": load('./models/prospectiveReference/prospective_decision_tree_mean_diff.joblib'),
        "XGBClassifier": load('./models/prospectiveReference/prospective_xgb_mean_diff.joblib'),
        "RandomForestClassifier": load('./models/prospectiveReference/prospective_random_forest_mean_diff.joblib'),
    }

    app.state.standard_models = {
        "LogisticRegression": load("./models/standard/lr.joblib"),
        "DecisionTreeClassifier": load("./models/standard/dt.joblib"),
        "XGBClassifier": load("./models/standard/xgb.joblib"),
        "RandomForestClassifier": load("./models/standard/rf.joblib"),
        # "RUSBoostClassifier": load("./models/standard/rus_boost.joblib"),
    }