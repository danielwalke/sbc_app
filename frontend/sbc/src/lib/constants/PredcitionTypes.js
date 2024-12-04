import {
    ENDPOINT_PROSPECTIVE_PREDICTION_DETAILS,
    ENDPOINT_PROSPECTIVE_PREDICTIONS,
    ENDPOINT_PROSPECTIVE_REF_PREDICTION_DETAILS,
    ENDPOINT_PROSPECTIVE_REF_PREDICTIONS,
    ENDPOINT_PROSPECTIVE_REF_THRESHOLDS,
    ENDPOINT_PROSPECTIVE_THRESHOLDS,
    ENDPOINT_RETROSPECTIVE_PREDICTION_DETAILS,
    ENDPOINT_RETROSPECTIVE_PREDICTIONS,
    ENDPOINT_RETROSPECTIVE_THRESHOLDS,
    ENDPOINT_STANDARD_PREDICTION_DETAILS,
    ENDPOINT_STANDARD_PREDICTIONS,
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
        "label": "prospective (ref.)",
        "value": "prospectiveRef",
    },
    {
        "label": "retrospective",
        "value": "retrospective",
    },

]

export const predictionTypeThresholdEndpoints = {
    "standard": ENDPOINT_STANDARD_THRESHOLDS,
    "prospective": ENDPOINT_PROSPECTIVE_THRESHOLDS,
    "retrospective": ENDPOINT_RETROSPECTIVE_THRESHOLDS,
    "prospectiveRef": ENDPOINT_PROSPECTIVE_REF_THRESHOLDS
}

export const predictionTypePredictionEndpoints = {
    "standard": ENDPOINT_STANDARD_PREDICTIONS,
    "prospective": ENDPOINT_PROSPECTIVE_PREDICTIONS,
    "retrospective": ENDPOINT_RETROSPECTIVE_PREDICTIONS,
    "prospectiveRef": ENDPOINT_PROSPECTIVE_REF_PREDICTIONS,
}

export const predictionTypePredictionDetailsEndpoints = {
    "standard": ENDPOINT_STANDARD_PREDICTION_DETAILS,
    "prospective": ENDPOINT_PROSPECTIVE_PREDICTION_DETAILS,
    "retrospective": ENDPOINT_RETROSPECTIVE_PREDICTION_DETAILS,
    "prospectiveRef": ENDPOINT_PROSPECTIVE_REF_PREDICTION_DETAILS,
}

export const predictionTypeCBCCallback = {
    "standard": getCbcInformation,
    "prospective": getGraphCbcInformation,
    "retrospective": getGraphCbcInformation,
    "prospectiveRef": getGraphCbcInformation,
}