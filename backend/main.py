from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
from service.impl.GraphPrediction import GraphPrediction
from service.impl.DetailsPreidctionGraph import DetailsPredictionGraph
from service.impl.Prediction import Prediction
from service.meta.OutPrediction import OutPrediction
from service.meta.CBC import CBC
from service.meta.GraphCBC import GraphCBC
from service.meta.OutDetailsPredictions import OutDetailsPredictions
from service.impl.DetailsPrediction import DetailsPrediction
import pandas as pd
from dataAnalysis.DataAnalysis import DataAnalysis
from sklearn.model_selection import train_test_split
from datetime import datetime
import os
from service.meta.InPrediction import InPrediction
from service.meta.InGraphPrediction import InGraphPrediction

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
    y_train = data_analysis.get_y_train()
    X_train = data_analysis.get_X_train()

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

    app.state.model = load('models/rf_limited_jobs.joblib')
    app.state.rf_model = app.state.model  # load('models/rf.joblib')
    app.state.dt_model = load('models/dt.joblib')
    app.state.lr_model = load('models/lr.joblib')
    app.state.xgb_model = load('models/xgb.joblib')
    app.state.classifiers = [app.state.rf_model, app.state.dt_model, app.state.lr_model, app.state.xgb_model]
    app.state.classifiers_dict = \
        {
            "RandomForestClassifier": app.state.rf_model,
            "XGBClassifier": app.state.xgb_model,
            "DecisionTreeClassifier": app.state.dt_model,
            "LogisticRegression": app.state.lr_model
        }
    app.state.classifier_thresholds = {
        "RandomForestClassifier": 0.3269368308502123,
        "XGBClassifier": 0.08329411,
        "DecisionTreeClassifier": 0.5479930767959986,
        "LogisticRegression": 0.4746955641186002,
        "GraphAware": 0.4776,
    }
    app.state.background_data = X_train

    graph_aware_clf_0 = load('models/graph_aware_rf_0.joblib')
    graph_aware_clf_1 = load('models/graph_aware_rf_1.joblib')
    app.state.graph_aware_clfs = [graph_aware_clf_0, graph_aware_clf_1]


@app.get(ADD_PATH)
def read_root():
    return {"Hello": "World"}


@app.get(ADD_PATH + "/classifier_thresholds")
async def get_classifier_thresholds():
    return app.state.classifier_thresholds


@app.post(ADD_PATH + "/get_pred/")
async def get_pred(in_prediction: InPrediction) -> OutPrediction:
    print(datetime.now())
    classifier = in_prediction.classifier
    cbc_items = in_prediction.data
    prediction = Prediction(cbc_items, app.state.classifiers_dict[classifier], app.state.classifier_thresholds)
    return prediction.get_output()


@app.post(ADD_PATH + "/get_pred_details/")
async def get_pred_details(cbc_items: list[CBC]) -> OutDetailsPredictions:
    prediction = DetailsPrediction(cbc_items, app.state.classifiers, app.state.classifier_thresholds,
                                   app.state.background_data)
    return prediction.get_output()


@app.post(ADD_PATH + "/get_graph_pred/")
async def get_graph_pred(in_prediction: InGraphPrediction) -> OutPrediction:
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    print(graph_cbc_items[0])
    prediction = GraphPrediction(graph_cbc_items, app.state.graph_aware_clfs, app.state.classifier_thresholds)
    return prediction.get_output()


@app.post(ADD_PATH + "/get_graph_pred_details/")
async def get_graph_pred_details(graph_cbc_items: list[GraphCBC]) -> OutDetailsPredictions:
    prediction = DetailsPredictionGraph(graph_cbc_items, app.state.graph_aware_clfs, app.state.classifier_thresholds)
    return prediction.get_output()
