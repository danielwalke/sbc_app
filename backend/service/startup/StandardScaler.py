from joblib import load


def initialize_standard_scaler(app):

    app.state.standard_scaler = {
        "prospective_sc": load("./models/prospective_sc.joblib"),
        "retrospective_sc": load("./models/retrospective_sc.joblib")
    }
