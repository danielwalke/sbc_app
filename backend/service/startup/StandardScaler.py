from joblib import load


def initialize_standard_scaler(app):
    ##TODO Change
    app.state.standard_scaler = {
        "prospective_sc": load("./models/prospective/prospective_sc.joblib"),
        "retrospective_sc": load("./models/retrospective/retrospective_sc.joblib"),
        "prospective_ref_sc": load("./models/prospective/prospective_sc.joblib") ##load("./models/retrospective/prospective_logistic_regression_mean_diff_sc.joblib")
    }
