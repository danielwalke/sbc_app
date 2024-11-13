import {useCbcStore} from "../stores/CbcStore.js";
import {submitCbcDetail} from "./CBCDetails.js";

export async function submitCbcClassifierDetails(){
    const store = useCbcStore()
    store.setIsLoading(true)
    store.setHasPredictionDetails(false)
    for(let i in store.cbcOverClassifiers){
        const selectedCbc = store.cbcOverClassifiers[i]
        await submitCbcDetail(selectedCbc, selectedCbc.classifier)
    }
}