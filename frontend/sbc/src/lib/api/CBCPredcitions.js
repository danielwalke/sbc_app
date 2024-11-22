import {useModalStore} from "../stores/ModalStore.js";
import {getCbcInformation} from "../cbcHelper/CBCApiFormat.js";
import {ENDPOINT_PROSPECTIVE_PREDICTIONS, ENDPOINT_RETROSPECTIVE_PREDICTIONS} from "../constants/Server.js";
import axios from "axios";
import {calculate_confidence_score} from "../cbcHelper/ConfidenceCalculation.js";
import {useCbcStore} from "../stores/CbcStore.js";
import {submitCbcDetail} from "./CBCDetails.js";

export function removeConfidenceFilters(){
    const modalStore = useModalStore()
    modalStore.setFilters(modalStore.getFilters.filter(filter => !["confidence"].includes(filter["filterKey"])))
}

export async function submitCbcMeasurements(){
    removeConfidenceFilters()
    const store = useCbcStore()
    store.setIsLoading(true)
    store.setHasPredictions(false)

    const data = store.getCbcMeasurements.map(c=> getCbcInformation(c))
    const endpoint = store.predictionType === "prospective" ? ENDPOINT_PROSPECTIVE_PREDICTIONS : ENDPOINT_RETROSPECTIVE_PREDICTIONS
    axios.post(endpoint, {data: data, classifier: "RandomForestClassifier"})
        .then(function (response) {
            store.setIsLoading(false)
            store.setHasPredictions(true)
            for(let i in store.getCbcMeasurements){
                const cbc = store.getCbcMeasurements[i]
                cbc.pred = response.data.predictions[i] ? 'Sepsis' : 'Control'
                cbc.pred_proba = response.data.pred_probas[i]
                cbc.confidence = Math.round(calculate_confidence_score(cbc.pred_proba, store.getClassifierThresholds["RandomForestClassifier"])*10000)/100
            }
            const cbcsWithDetails = store.getCbcMeasurements.filter(cbc => cbc.chartData)
            for(const cbc of cbcsWithDetails){
                submitCbcDetail(cbc)
            }
        })
}