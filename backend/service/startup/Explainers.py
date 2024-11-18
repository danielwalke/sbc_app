import shap
import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis
from service.impl.GraphPrediction import GraphPrediction
from service.meta.GraphCBC import GraphCBC
import torch
from typing import List

def get_background_data_cbc_items():
    data = pd.read_csv(r"./extdata/sbcdata.csv", header=0)
    data_analysis = DataAnalysis(data)
    training_data = data_analysis.get_training_data()
    train_data_filtered = training_data.loc[:.5 * training_data.shape[0],
                          ["Id", "Time", "Age", "Sex", "HGB", "WBC", "RBC", "MCV", "PLT", "Label"]]
    train_data_filtered["Label"] = train_data_filtered["Label"] == "Sepsis"
    train_data_filtered = train_data_filtered.rename(
        columns={"Id": "id", "Time": "order", "Age": "age", "Sex": "sex", "Label": "ground_truth"})
    graph_cbc_items: List[GraphCBC] = [GraphCBC(**row) for row in train_data_filtered.to_dict(orient="records")]
    return graph_cbc_items


def get_prospective_background_data(app, graph_cbc_items):
    graph_constr = GraphPrediction(graph_cbc_items, None, None, None)
    graph_constr.construct_directed_graph()
    features_origin, features_time = graph_constr.get_features_list()
    prospective_background_data = torch.cat([features_origin, features_time], dim=-1).cpu().numpy()
    prospective_background_data = app.state.standard_scaler["prospective_sc"].transform(prospective_background_data)
    return prospective_background_data


def get_retrospective_background_data(app, graph_cbc_items):
    graph_constr = GraphPrediction(graph_cbc_items, None, None, None)
    graph_constr.construct_reversed_directed_graph()
    features_origin, features_time = graph_constr.get_features_list()
    retrospective_background_data = torch.cat([features_origin, features_time], dim=-1).cpu().numpy()
    retrospective_background_data = app.state.standard_scaler["retrospective_sc"].transform(
        retrospective_background_data)
    return retrospective_background_data


def initialize_explainers(app):
    graph_cbc_items = get_background_data_cbc_items()
    prospective_background_data = get_prospective_background_data(app, graph_cbc_items)
    retrospective_background_data = get_retrospective_background_data(app, graph_cbc_items)

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