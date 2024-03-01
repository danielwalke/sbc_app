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

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    data = pd.read_csv(r"./extdata/sbcdata.csv", header=0)
    data_analysis = DataAnalysis(data)
    y_train = data_analysis.get_y_train()
    X_train = data_analysis.get_X_train()

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

    app.state.model = load('models/rf.joblib')
    app.state.rf_model = app.state.model #load('models/rf.joblib')
    app.state.dt_model = load('models/dt.joblib')
    app.state.lr_model = load('models/lr.joblib')
    app.state.xgb_model = load('models/xgb.joblib')
    app.state.classifiers = [app.state.rf_model, app.state.dt_model, app.state.lr_model, app.state.xgb_model]
    app.state.classifier_thresholds = {
        "RandomForestClassifier": 0.3269368308502123,
        "XGBClassifier": 0.08329411,
        "DecisionTreeClassifier": 0.5479930767959986,
        "LogisticRegression": 0.4746955641186002,
    }
    app.state.background_data = X_train

    graph_aware_clf_0 = load('models/graph_aware_rf_0.joblib')
    graph_aware_clf_1 = load('models/graph_aware_rf_1.joblib')
    app.state.graph_aware_clfs = [graph_aware_clf_0, graph_aware_clf_1]



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/classifier_thresholds")
async def get_classifier_thresholds():
    return app.state.classifier_thresholds


@app.post("/get_pred/")
async def get_pred(cbc_items: list[CBC]) -> OutPrediction:
    print(cbc_items)
    prediction = Prediction(cbc_items, app.state.model, app.state.classifier_thresholds)
    return prediction.get_output()


@app.post("/get_pred_details/")
async def get_pred_details(cbc_items: list[CBC]) -> OutDetailsPredictions:
    print(cbc_items)
    prediction = DetailsPrediction(cbc_items, app.state.classifiers, app.state.classifier_thresholds,
                                   app.state.background_data)
    return prediction.get_output()


# @app.post("/get_graph_pred/")
# async def get_graph_pred(graph_cbc_items: list[GraphCBC]) -> OutPrediction:
#     prediction = GraphPrediction(graph_cbc_items, app.state.graph_aware_clfs)
#     return prediction.get_output()
