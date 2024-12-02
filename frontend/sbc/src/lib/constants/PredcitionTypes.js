import {
    ENDPOINT_PROSPECTIVE_PREDICTION_DETAILS,
    ENDPOINT_PROSPECTIVE_PREDICTIONS,
    ENDPOINT_PROSPECTIVE_THRESHOLDS, ENDPOINT_RETROSPECTIVE_PREDICTION_DETAILS, ENDPOINT_RETROSPECTIVE_PREDICTIONS,
    ENDPOINT_RETROSPECTIVE_THRESHOLDS, ENDPOINT_STANDARD_PREDICTION_DETAILS, ENDPOINT_STANDARD_PREDICTIONS,
    ENDPOINT_STANDARD_THRESHOLDS
} from "./Server.js";
import {getCbcInformation, getGraphCbcInformation} from "../cbcHelper/CBCApiFormat.js";

export const predictionTypes = [
    {
        "label": "standard",
        "value": "standard",
    },
    {
        "label": "prospective",
        "value": "prospective",
    },
    {
        "label": "retrospective",
        "value": "retrospective",
    },

]

export const predictionTypeThresholdEndpoints = {
    "standard": ENDPOINT_STANDARD_THRESHOLDS,
    "prospective": ENDPOINT_PROSPECTIVE_THRESHOLDS,
    "retrospective": ENDPOINT_RETROSPECTIVE_THRESHOLDS
}

export const predictionTypePredictionEndpoints = {
    "standard": ENDPOINT_STANDARD_PREDICTIONS,
    "prospective": ENDPOINT_PROSPECTIVE_PREDICTIONS,
    "retrospective": ENDPOINT_RETROSPECTIVE_PREDICTIONS
}

export const predictionTypePredictionDetailsEndpoints = {
    "standard": ENDPOINT_STANDARD_PREDICTION_DETAILS,
    "prospective": ENDPOINT_PROSPECTIVE_PREDICTION_DETAILS,
    "retrospective": ENDPOINT_RETROSPECTIVE_PREDICTION_DETAILS
}

export const predictionTypeCBCCallback = {
    "standard": getCbcInformation,
    "prospective": getGraphCbcInformation,
    "retrospective": getGraphCbcInformation
}