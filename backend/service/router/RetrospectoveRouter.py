from fastapi import APIRouter, Request
import pandas as pd
from service.meta.GraphCBC import GraphCBC
from service.constants.Server import ADD_PATH
from service.meta.InGraphPrediction import InGraphPrediction
from service.meta.InThreshold import InThreshold
from service.impl.ThresholdCalculation import ThresholdCalculation
from service.impl.GraphPrediction import GraphPrediction
from service.impl.DetailsPredictionGraph import DetailsPredictionGraph

router = APIRouter(redirect_slashes=False)


@router.post(ADD_PATH + "/classifier_thresholds_retrospective")
async def get_classifier_thresholds_retrospective(request: Request, body:InThreshold):
    threshold_calculation = ThresholdCalculation(request.app.state.retrospective_df,
                                                 request.app.state.retrospective_thresholds,
                                                 body.min_sensitivity)
    return threshold_calculation.get_thresholds()


@router.post(ADD_PATH + "/get_graph_pred_retrospective")
async def get_graph_pred_retrospective(request: Request, in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    prediction = GraphPrediction(graph_cbc_items, request.app.state.retrospective_models[in_prediction.classifier],
                                 request.app.state.retrospective_thresholds[in_prediction.classifier], None)
    return prediction.get_retrospective_output()


@router.post(ADD_PATH + "/get_graph_pred_details_retrospective")
async def get_graph_pred_details_retrospective(request: Request, in_prediction: InGraphPrediction):
    graph_cbc_items: list[GraphCBC] = in_prediction.data
    standard_scaler = request.app.state.standard_scaler[
        "retrospective_sc"] if in_prediction.classifier == "LogisticRegression" else None
    prediction = DetailsPredictionGraph(graph_cbc_items,
                                        request.app.state.retrospective_models[in_prediction.classifier],
                                        request.app.state.retrospective_explainers[in_prediction.classifier],
                                        request.app.state.retrospective_thresholds[in_prediction.classifier],
                                        standard_scaler)
    return prediction.get_retrospective_output()
