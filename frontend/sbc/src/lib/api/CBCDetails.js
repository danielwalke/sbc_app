import axios from "axios";
import {useCbcStore} from "../stores/CbcStore.js";
import {calculate_confidence_score} from "../cbcHelper/ConfidenceCalculation.js";
import {getShapFormat} from "../shap/ChartFormat.js";
import {predictionTypeCBCCallback, predictionTypePredictionDetailsEndpoints} from "../constants/PredcitionTypes.js";
import {DEFAULT_CLASSIFIER} from "../constants/Server.js";

async function standardDetailSubmission(store, selected_cbc, classifier, endpoint){
    const data = predictionTypeCBCCallback[store.predictionType](selected_cbc)
    axios.post(endpoint, {data: data, classifier: classifier, threshold: store.getClassifierThresholds[classifier]},{
        timeout: 10000 // Timeout set to 10 seconds
    })
        .then(function (response) {
            store.setIsLoading(false)
            selected_cbc.pred = response.data.prediction ? 'Sepsis' : 'Control'
            selected_cbc.pred_proba = response.data.pred_proba
            selected_cbc.confidence = Math.round(calculate_confidence_score(selected_cbc.pred_proba, store.getClassifierThresholds[classifier])*10000)/100
            const shap_values_comb = response.data.shap_values
            selected_cbc.chartData = {}
            selected_cbc.chartData["combined"] = getShapFormat(shap_values_comb)
        })
        .catch((e)=>{
            console.error(`Could not fetch standard details for ${classifier}`)
            console.error(e)
        })
}

async function graphDetailSubmission(store, selected_cbc, classifier, endpoint){
    const associatedCbcs = store.cbcMeasurements.filter(cbc => cbc.patientId === selected_cbc.patientId)
    const associatedUuids = associatedCbcs.map(cbc => cbc.id)
    const selectedCbcIdx = associatedUuids.indexOf(selected_cbc.id)
    const data = associatedCbcs.map(cbc => predictionTypeCBCCallback[store.predictionType](cbc))

    axios.post(endpoint, {data: data, classifier: classifier, threshold: store.getClassifierThresholds[classifier]},{
        timeout: 10000 // Timeout set to 10 seconds
    })
        .then(function (response) {
            store.setIsLoading(false)
            const prediction_detail = response.data.prediction_detail
            selected_cbc.pred = prediction_detail.predictions[selectedCbcIdx] ? 'Sepsis' : 'Control'
            selected_cbc.pred_proba = prediction_detail.pred_probas[selectedCbcIdx]
            selected_cbc.confidence = Math.round(calculate_confidence_score(selected_cbc.pred_proba, store.getClassifierThresholds[classifier])*10000)/100
            console.log(prediction_detail.shap_values_list["combined"])
            const shap_values_comb = prediction_detail.shap_values_list["combined"][selectedCbcIdx]
            const shap_values_time = prediction_detail.shap_values_list["time"][selectedCbcIdx]
            const shap_values_origin = prediction_detail.shap_values_list["original"][selectedCbcIdx]
            selected_cbc.chartData = {}
            selected_cbc.chartData["combined"] = getShapFormat(shap_values_comb)
            selected_cbc.chartData["time"] = associatedCbcs.length > 1 ? getShapFormat(shap_values_time) : undefined
            selected_cbc.chartData["original"] = associatedCbcs.length > 1 ? getShapFormat(shap_values_origin) : undefined
        })
        .catch((e)=>{
            console.error(`Could not fetch details for ${classifier}`)
            console.error(e)
        })
}

export async function submitCbcDetail(selected_cbc, classifier = DEFAULT_CLASSIFIER){
    const store = useCbcStore()
    store.setIsLoading(true)
    const endpoint = predictionTypePredictionDetailsEndpoints[store.predictionType]
    if(store.predictionType === "standard"){
        return await standardDetailSubmission(store, selected_cbc, classifier, endpoint)
    }
    return await graphDetailSubmission(store, selected_cbc, classifier, endpoint)
}