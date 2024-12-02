import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from service.meta.OutPrediction import OutPrediction
from service.meta.InPrediction import InPrediction
from service.meta.GraphCBC import GraphCBC
from service.meta.OutDetailsPrediction import OutDetailsPrediction
from service.meta.InGraphPrediction import InGraphPrediction
from service.meta.CBC import CBC
from service.meta.InPredictionDetails import InPredictionDetails

from service.impl.GraphPrediction import GraphPrediction
from service.impl.DetailsPredictionGraph import DetailsPredictionGraph
from service.impl.Prediction import Prediction
from service.impl.PredictionDetails import PredictionDetails

from service.startup.StandardScaler import initialize_standard_scaler
from service.startup.Thresholds import initialize_thresholds
from service.startup.Models import initialize_models
from service.startup.Explainers import initialize_explainers

from fastapi import APIRouter

os.environ["OPENBLAS_NUM_THREADS"] = '8'
ADD_PATH = "/sbc-shap"
app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
# app.add_middleware(HTTPSRedirectMiddleware)
router = APIRouter(redirect_slashes=False)


@app.on_event("startup")
async def startup_event():
    initialize_standard_scaler(app)
    initialize_thresholds(app)
    initialize_models(app)
    initialize_explainers(app)


@router.get(ADD_PATH)
def read_root():
    return {"Hello": "World"}


@router.get(ADD_PATH + "/classifier_thresholds_retrospective")
async def get_classifier_thresholds_retrospective():
    return app.state.retrospective_thresholds


@router.get(ADD_PATH + "/classifier_thresholds_prospective")
async def get_classifier_thresholds_prospective():
    return app.state.prospective_thresholds


@router.get(ADD_PATH + "/classifier_thresholds_standard")
async def get_classifier_thresholds_standard():
    return app.state.standard_thresholds


@router.post(ADD_PATH + "/get_graph_pred_prospective")
async def get_graph_pred_prospective(in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    print(graph_cbc_items[0])
    prediction = GraphPrediction(graph_cbc_items, app.state.prospective_models[in_prediction.classifier],
                                 app.state.prospective_thresholds[in_prediction.classifier], None)
    return prediction.get_prospective_output()


@router.post(ADD_PATH + "/get_graph_pred_retrospective")
async def get_graph_pred_retrospective(in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    print(graph_cbc_items[0])
    prediction = GraphPrediction(graph_cbc_items, app.state.retrospective_models[in_prediction.classifier],
                                 app.state.retrospective_thresholds[in_prediction.classifier], None)
    return prediction.get_retrospective_output()


@router.post(ADD_PATH + "/get_graph_pred_details_retrospective")
async def get_graph_pred_details_retrospective(in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    standard_scaler = app.state.standard_scaler[
        "retrospective_sc"] if in_prediction.classifier == "LogisticRegression" else None
    prediction = DetailsPredictionGraph(graph_cbc_items, app.state.retrospective_models[in_prediction.classifier],
                                        app.state.retrospective_explainers[in_prediction.classifier],
                                        app.state.retrospective_thresholds[in_prediction.classifier],
                                        standard_scaler)
    return prediction.get_retrospective_output()


@router.post(ADD_PATH + "/get_graph_pred_details_prospective")
async def get_graph_pred_details_prospective(in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    standard_scaler = app.state.standard_scaler[
        "prospective_sc"] if in_prediction.classifier == "LogisticRegression" else None
    prediction = DetailsPredictionGraph(graph_cbc_items, app.state.prospective_models[in_prediction.classifier],
                                        app.state.prospective_explainers[in_prediction.classifier],
                                        app.state.prospective_thresholds[in_prediction.classifier],
                                        standard_scaler)
    return prediction.get_prospective_output()


@router.post(ADD_PATH + "/get_standard_pred")
async def get_standard_pred(in_prediction: InPrediction):
    cbc_items: list[CBC] = in_prediction.data
    prediction = Prediction(cbc_items, app.state.standard_models[in_prediction.classifier],
                            app.state.standard_thresholds[in_prediction.classifier])
    return prediction.get_output()


@router.post(ADD_PATH + "/get_standard_pred_details")
async def get_standard_pred_details(in_prediction: InPredictionDetails):
    cbc_item:  CBC = in_prediction.data
    prediction_details = PredictionDetails(cbc_item,
                                            app.state.standard_models[in_prediction.classifier],
                                            app.state.standard_thresholds[in_prediction.classifier],
                                            app.state.standard_explainers[in_prediction.classifier])
    return prediction_details.get_detailed_output()


app.include_router(router)
