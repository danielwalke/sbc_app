from fastapi import APIRouter, Request
import pandas as pd
from service.meta.GraphCBC import GraphCBC
from service.meta.InThreshold import InThreshold
from service.impl.ThresholdCalculation import ThresholdCalculation
from service.constants.Server import ADD_PATH
from service.meta.InGraphPrediction import InGraphPrediction
from service.impl.GraphPrediction import GraphPrediction
from service.impl.DetailsPredictionGraph import DetailsPredictionGraph

router = APIRouter(redirect_slashes=False)


@router.post(ADD_PATH + "/classifier_thresholds_prospective")
async def get_classifier_thresholds_prospective(request: Request, body:InThreshold):
    threshold_calculation = ThresholdCalculation(request.app.state.prospective_df,
                                                 request.app.state.prospective_thresholds,
                                                 body.min_sensitivity)
    return threshold_calculation.get_thresholds()


@router.post(ADD_PATH + "/get_graph_pred_prospective")
async def get_graph_pred_prospective(request: Request, in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    standard_scaler = request.app.state.standard_scaler[
        "prospective_sc"] if in_prediction.classifier == "LogisticRegression" else None
    prediction = GraphPrediction(graph_cbc_items, request.app.state.prospective_models[in_prediction.classifier],
                                 request.app.state.prospective_thresholds[in_prediction.classifier], standard_scaler)
    return prediction.get_prospective_output()


@router.post(ADD_PATH + "/get_graph_pred_details_prospective")
async def get_graph_pred_details_prospective(request: Request, in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    standard_scaler = request.app.state.standard_scaler[
        "prospective_sc"] if in_prediction.classifier == "LogisticRegression" else None
    prediction = DetailsPredictionGraph(graph_cbc_items, request.app.state.prospective_models[in_prediction.classifier],
                                        request.app.state.prospective_explainers[in_prediction.classifier],
                                        request.app.state.prospective_thresholds[in_prediction.classifier],
                                        standard_scaler)
    return prediction.get_prospective_output()
