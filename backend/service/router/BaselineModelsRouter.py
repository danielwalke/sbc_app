import pandas as pd
from fastapi import APIRouter, Request
from service.constants.Server import ADD_PATH
from service.impl.ThresholdCalculation import ThresholdCalculation
from service.meta.CBC import CBC
from service.meta.InPredictionDetails import InPredictionDetails
from service.meta.InPrediction import InPrediction
from service.meta.InThreshold import InThreshold
from service.impl.Prediction import Prediction
from service.impl.PredictionDetails import PredictionDetails


router = APIRouter(redirect_slashes=False)


@router.post(ADD_PATH + "/classifier_thresholds_standard")
async def get_classifier_thresholds_standard(request: Request, body:InThreshold):
    threshold_calculation = ThresholdCalculation(request.app.state.baseline_df, request.app.state.standard_thresholds, body.min_sensitivity)
    return threshold_calculation.get_thresholds()


@router.post(ADD_PATH + "/get_standard_pred")
async def get_standard_pred(request: Request, body: InPrediction):
    cbc_items: list[CBC] = body.data
    threshold:float = body.threshold
    prediction = Prediction(cbc_items, request.app.state.standard_models[body.classifier],
                            threshold)
    return prediction.get_output()


@router.post(ADD_PATH + "/get_standard_pred_details")
async def get_standard_pred_details(request: Request, body: InPredictionDetails):
    cbc_item: CBC = body.data
    threshold: float = body.threshold
    prediction_details = PredictionDetails(cbc_item,
                                           request.app.state.standard_models[body.classifier],
                                           threshold,
                                           request.app.state.standard_explainers[body.classifier])
    return prediction_details.get_detailed_output()
