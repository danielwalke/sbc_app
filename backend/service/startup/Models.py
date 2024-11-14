from joblib import load


def initialize_models(app):
    app.state.prospective_models = {
        "LogisticRegression": load('./models/prospective_logistic_regression.joblib'),
        "DecisionTreeClassifier": load('./models/prospective_decision_tree.joblib'),
        "XGBClassifier": load('./models/prospective_xgb.joblib'),
        "RandomForestClassifier": load('./models/prospective_random_forest.joblib'),
    }

    app.state.retrospective_models = {
        "LogisticRegression": load('./models/retrospective_logistic_regression.joblib'),
        "DecisionTreeClassifier": load('./models/retrospective_decision_tree.joblib'),
        "XGBClassifier": load('./models/retrospective_xgb.joblib'),
        "RandomForestClassifier": load('./models/retrospective_random_forest.joblib'),
    }