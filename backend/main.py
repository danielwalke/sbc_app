from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from torch.nn.functional import normalize
from joblib import load
from service.impl.Prediction import Prediction
from service.meta.OutPrediction import OutPrediction
from service.meta.CBC import CBC
from service.meta.GraphCBC import GraphCBC
from service.meta.OutDetailsPredictions import OutDetailsPredictions
from service.impl.DetailsPrediction import DetailsPrediction
import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis
from sklearn.model_selection import train_test_split
import shap
from datetime import datetime
import os
from service.meta.InPrediction import InPrediction
from service.meta.InGraphPrediction import InGraphPrediction
from service.impl.GraphPrediction import GraphPrediction
from service.impl.DetailsPredictionGraph import DetailsPredictionGraph
import torch
from service.constants import Thresholds
import numpy as np

os.environ["OPENBLAS_NUM_THREADS"] = '8'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADD_PATH = "/sbc"


@app.on_event("startup")
async def startup_event():
    data = pd.read_csv(r"./extdata/sbcdata.csv", header=0)
    data_analysis = DataAnalysis(data)
    training_data = data_analysis.get_training_data()
    ##TODO increase background data size
    train_data_filtered = training_data.loc[:.1*training_data.shape[0],["Id", "Time", "Age", "Sex", "HGB", "WBC","RBC", "MCV", "PLT", "Label"]]
    train_data_filtered["Label"] = train_data_filtered["Label"] == "Sepsis"
    train_data_filtered = train_data_filtered.rename(columns = {"Id": "id", "Time": "order", "Age": "age", "Sex": "sex", "Label": "ground_truth"})
    graph_cbc_items: List[GraphCBC] = [GraphCBC(**row) for row in train_data_filtered.to_dict(orient="records")]
    graph_constr = GraphPrediction(graph_cbc_items, None, None)
    graph_constr.construct_directed_graph()
    features_origin, features_time = graph_constr.get_features_list()
    prospective_background_data = torch.cat([features_origin, features_time], dim = -1)
    graph_constr.construct_reversed_directed_graph()
    features_origin, features_time = graph_constr.get_features_list()
    retrospective_background_data = torch.cat([features_origin, features_time], dim=-1)

    app.state.prospective_models = {
        "LogisticRegression":  load('models/prospective_logistic_regression.joblib'),
        "DecisionTreeClassifier": load('models/prospective_decision_tree.joblib'),
        "XGBClassifier": load('models/prospective_xgb.joblib'),
        "RandomForestClassifier": load('models/prospective_random_forest.joblib'),
    }
    app.state.prospective_thresholds = {
        "LogisticRegression": Thresholds.PROSPECTIVE_LR,
        "DecisionTreeClassifier": Thresholds.PROSPECTIVE_DT,
        "RandomForestClassifier": Thresholds.PROSPECTIVE_RF,
        "XGBClassifier": Thresholds.PROSPECTIVE_XGB,
    }
    app.state.retrospective_models = {
        "LogisticRegression": load('models/retrospective_logistic_regression.joblib'),
        "DecisionTreeClassifier": load('models/retrospective_decision_tree.joblib'),
        "XGBClassifier": load('models/retrospective_xgb.joblib'),
        "RandomForestClassifier": load('models/retrospective_random_forest.joblib'),
    }

    app.state.retrospective_thresholds = {
        "LogisticRegression": Thresholds.RETROSPECTIVE_LR,
        "DecisionTreeClassifier": Thresholds.RETROSPECTIVE_DT,
        "RandomForestClassifier": Thresholds.RETROSPECTIVE_RF,
        "XGBClassifier": Thresholds.RETROSPECTIVE_XGB,
    }

    app.state.retrospective_explainers = {
        "LogisticRegression": shap.LinearExplainer(app.state.retrospective_models["LogisticRegression"],
                                                   retrospective_background_data.cpu().numpy()),
        "DecisionTreeClassifier": shap.TreeExplainer(app.state.retrospective_models["DecisionTreeClassifier"]),
        "RandomForestClassifier": shap.TreeExplainer(app.state.retrospective_models["RandomForestClassifier"]),
        "XGBClassifier": shap.TreeExplainer(app.state.retrospective_models["XGBClassifier"]),
    }

    app.state.prospective_explainers = {
        "LogisticRegression": shap.LinearExplainer(app.state.prospective_models["LogisticRegression"],
                                                   prospective_background_data.cpu().numpy()),
        "DecisionTreeClassifier": shap.TreeExplainer(app.state.prospective_models["DecisionTreeClassifier"]),
        "RandomForestClassifier": shap.TreeExplainer(app.state.prospective_models["RandomForestClassifier"]),
        "XGBClassifier": shap.TreeExplainer(app.state.prospective_models["XGBClassifier"]),
    }

@app.get(ADD_PATH)
def read_root():
    return {"Hello": "World"}

@app.get(ADD_PATH + "/classifier_thresholds_retrospective")
async def get_classifier_thresholds_retrospective():
    return app.state.retrospective_thresholds

@app.get(ADD_PATH + "/classifier_thresholds_prospective")
async def get_classifier_thresholds_prospective():
    return app.state.prospective_thresholds

@app.post(ADD_PATH + "/get_graph_pred_prospective/")
async def get_graph_pred_prospective(in_prediction: InGraphPrediction) -> OutPrediction:
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    print(graph_cbc_items[0])
    prediction = GraphPrediction(graph_cbc_items, app.state.prospective_models[in_prediction.classifier], app.state.prospective_thresholds[in_prediction.classifier])
    return prediction.get_prospective_output()


@app.post(ADD_PATH + "/get_graph_pred_retrospective/")
async def get_graph_pred_retrospective(in_prediction: InGraphPrediction) -> OutPrediction:
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    print(graph_cbc_items[0])
    prediction = GraphPrediction(graph_cbc_items, app.state.retrospective_models[in_prediction.classifier], app.state.retrospective_thresholds[in_prediction.classifier])
    return prediction.get_retrospective_output()


@app.post(ADD_PATH + "/get_graph_pred_details_retrospective/")
async def get_graph_pred_details_retrospective(in_prediction: InGraphPrediction) -> OutDetailsPredictions:
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    prediction = DetailsPredictionGraph(graph_cbc_items, app.state.retrospective_models[in_prediction.classifier],app.state.retrospective_explainers[in_prediction.classifier], app.state.retrospective_thresholds[in_prediction.classifier])
    return prediction.get_retrospective_output()

@app.post(ADD_PATH + "/get_graph_pred_details_prospective/")
async def get_graph_pred_details_prospective(in_prediction: InGraphPrediction) -> OutDetailsPredictions:
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    prediction = DetailsPredictionGraph(graph_cbc_items,app.state.prospective_models[in_prediction.classifier],app.state.prospective_explainers[in_prediction.classifier], app.state.prospective_thresholds[in_prediction.classifier])
    return prediction.get_prospective_output()