import shap
import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis
from service.impl.GraphPrediction import GraphPrediction
from service.impl.Prediction import Prediction
from service.meta.GraphCBC import GraphCBC
from service.meta.CBC import CBC
import torch
from typing import List
from service.startup import RefNodes


def get_background_data():
    data = pd.read_csv(r"./extdata/sbcdata.csv", header=0)
    data_analysis = DataAnalysis(data)
    training_data = data_analysis.get_training_data()
    ## TODO Increase background data for logistic regression
    train_data_filtered = training_data.loc[:.5 * training_data.shape[0], :]
    return train_data_filtered


def get_background_data_cbc_items():
    background_data = get_background_data()
    train_data_filtered = background_data.loc[:,
                          ["Id", "Time", "Age", "Sex", "HGB", "WBC", "RBC", "MCV", "PLT", "Label"]]
    train_data_filtered["Label"] = train_data_filtered["Label"] == "Sepsis"
    train_data_filtered = train_data_filtered.rename(
        columns={"Id": "id", "Time": "order", "Age": "age", "Sex": "sex", "Label": "ground_truth"})
    graph_cbc_items: List[GraphCBC] = [GraphCBC(**row) for row in train_data_filtered.to_dict(orient="records")]
    return graph_cbc_items


def get_prospective_background_data(app, graph_constr, scaler):
    graph_constr.construct_directed_graph()
    features_origin, features_time = graph_constr.get_features_list()
    prospective_background_data = torch.cat([features_origin, features_time], dim=-1).cpu().numpy()
    prospective_background_data = scaler.transform(prospective_background_data)
    return prospective_background_data


def get_retrospective_background_data(app, graph_constr):
    graph_constr.construct_reversed_directed_graph()
    features_origin, features_time = graph_constr.get_features_list()
    retrospective_background_data = torch.cat([features_origin, features_time], dim=-1).cpu().numpy()
    retrospective_background_data = app.state.standard_scaler["retrospective_sc"].transform(
        retrospective_background_data)
    return retrospective_background_data


def get_standard_background_data():
    background_data = get_background_data()
    train_data_filtered = background_data.loc[:, ["Age", "Sex", "HGB", "WBC", "RBC", "MCV", "PLT", "Label"]]
    train_data_filtered["Label"] = train_data_filtered["Label"] == "Sepsis"
    train_data_filtered = train_data_filtered.rename(columns={"Age": "age", "Sex": "sex", "Label": "ground_truth"})
    cbc_items: List[CBC] = [CBC(**row) for row in train_data_filtered.to_dict(orient="records")]
    feature_constr = Prediction(cbc_items, None, None)
    return feature_constr.get_features()


def initialize_explainers(app):
    graph_cbc_items = get_background_data_cbc_items()
    graph_constr = GraphPrediction(graph_cbc_items, None, None, None, None)
    prospective_background_data = get_prospective_background_data(app, graph_constr, app.state.standard_scaler["prospective_sc"])
    retrospective_background_data = get_retrospective_background_data(app, graph_constr)

    graph_constr_ref_node = GraphPrediction(graph_cbc_items, None, None, None, app.state.mean_ref_node)
    prospective_ref_background_data = get_prospective_background_data(app, graph_constr_ref_node, app.state.standard_scaler["prospective_ref_sc"])

    standard_background_data = get_standard_background_data()

    app.state.retrospective_explainers = {
        "LogisticRegression": shap.LinearExplainer(app.state.retrospective_models["LogisticRegression"],
                                                   retrospective_background_data),
        "DecisionTreeClassifier": shap.TreeExplainer(app.state.retrospective_models["DecisionTreeClassifier"]),
        "RandomForestClassifier": shap.TreeExplainer(app.state.retrospective_models["RandomForestClassifier"]),
        "XGBClassifier": shap.TreeExplainer(app.state.retrospective_models["XGBClassifier"]),
    }

    app.state.prospective_explainers = {
        "LogisticRegression": shap.LinearExplainer(app.state.prospective_models["LogisticRegression"],
                                                   prospective_background_data),
        "DecisionTreeClassifier": shap.TreeExplainer(app.state.prospective_models["DecisionTreeClassifier"]),
        "RandomForestClassifier": shap.TreeExplainer(app.state.prospective_models["RandomForestClassifier"]),
        "XGBClassifier": shap.TreeExplainer(app.state.prospective_models["XGBClassifier"]),
    }

    app.state.prospective_ref_explainers = {
        "LogisticRegression": shap.LinearExplainer(app.state.prospective_ref_models["LogisticRegression"],
                                                   prospective_ref_background_data),
        "DecisionTreeClassifier": shap.TreeExplainer(app.state.prospective_ref_models["DecisionTreeClassifier"]),
        "RandomForestClassifier": shap.TreeExplainer(app.state.prospective_ref_models["RandomForestClassifier"]),
        "XGBClassifier": shap.TreeExplainer(app.state.prospective_ref_models["XGBClassifier"]),
    }

    app.state.standard_explainers = {
        "LogisticRegression": shap.LinearExplainer(app.state.standard_models["LogisticRegression"],
                                                   standard_background_data),
        "DecisionTreeClassifier": shap.TreeExplainer(app.state.standard_models["DecisionTreeClassifier"]),
        "RandomForestClassifier": shap.TreeExplainer(app.state.standard_models["RandomForestClassifier"]),
        "XGBClassifier": shap.TreeExplainer(app.state.standard_models["XGBClassifier"]),
        # "RUSBoostClassifier": shap.TreeExplainer(app.state.standard_models["RUSBoostClassifier"]),
    }
