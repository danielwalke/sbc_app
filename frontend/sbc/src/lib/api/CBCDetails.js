import {
    ENDPOINT_PROSPECTIVE_PREDICTION_DETAILS,
    ENDPOINT_RETROSPECTIVE_PREDICTION_DETAILS
} from "../constants/Server.js";
import axios from "axios";
import {useCbcStore} from "../stores/CbcStore.js";
import {getCbcInformation} from "../cbcHelper/CBCApiFormat.js";
import {calculate_confidence_score} from "../cbcHelper/ConfidenceCalculation.js";
import {getShapFormat} from "../shap/ChartFormat.js";

export async function submitCbcDetail(selected_cbc, classifier = "RandomForestClassifier"){
    const store = useCbcStore()
    store.setIsLoading(true)
    const endpoint = store.predictionType === "prospective" ? ENDPOINT_PROSPECTIVE_PREDICTION_DETAILS : ENDPOINT_RETROSPECTIVE_PREDICTION_DETAILS
    const associatedCbcs = store.cbcMeasurements.filter(cbc => cbc.patientId === selected_cbc.patientId)
    const associatedUuids = associatedCbcs.map(cbc => cbc.id)
    const selectedCbcIdx = associatedUuids.indexOf(selected_cbc.id)
    const data = associatedCbcs.map(cbc => getCbcInformation(cbc))
    axios.post(endpoint, {data: data, classifier: classifier})
        .then(function (response) {
            store.setIsLoading(false)
            const prediction_detail = response.data.prediction_detail
            selected_cbc.pred = prediction_detail.predictions[selectedCbcIdx] ? 'Sepsis' : 'Control'
            selected_cbc.pred_proba = prediction_detail.pred_probas[selectedCbcIdx]
            selected_cbc.confidence = Math.round(calculate_confidence_score(selected_cbc.pred_proba, store.getClassifierThresholds[classifier])*10000)/100
            const shap_values_comb = Array.isArray(prediction_detail.shap_values_list["combined"][0])  ? prediction_detail.shap_values_list["combined"][selectedCbcIdx] : prediction_detail.shap_values_list["combined"]
            const shap_values_time = Array.isArray(prediction_detail.shap_values_list["time"][0])  ? prediction_detail.shap_values_list["time"][selectedCbcIdx] : prediction_detail.shap_values_list["time"]
            const shap_values_origin = Array.isArray(prediction_detail.shap_values_list["original"][0])  ? prediction_detail.shap_values_list["original"][selectedCbcIdx] : prediction_detail.shap_values_list["original"]
            selected_cbc.chartData = {}
            selected_cbc.chartData["combined"] = getShapFormat(shap_values_comb)
            selected_cbc.chartData["time"] = getShapFormat(shap_values_time)
            selected_cbc.chartData["original"] = getShapFormat(shap_values_origin)
        })
        .catch((e)=>{
            console.error(`Could not fetch details for ${classifier}`)
            console.error(e)
        })
}