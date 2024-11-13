import {ENDPOINT_PROSPECTIVE_THRESHOLDS, ENDPOINT_RETROSPECTIVE_THRESHOLDS} from "../constants/Server.js";
import axios from "axios";
import {useCbcStore} from "../stores/CbcStore.js";

export async function fetchClassifierNamesAndThresholds(){
    const store = useCbcStore()
    store.setIsLoading(true)
    const classifier_endpoint = store.predictionType === "prospective" ? ENDPOINT_PROSPECTIVE_THRESHOLDS : ENDPOINT_RETROSPECTIVE_THRESHOLDS
    try{
        const response = await axios.get(classifier_endpoint)
        store.setClassifierNames(Object.keys(response.data))
        store.setClassifierThresholds(response.data)
        store.setIsLoading(false)
    }catch (e){
        console.error(e)
    }
}