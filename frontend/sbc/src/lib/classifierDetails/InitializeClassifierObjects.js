import {useRoute} from "vue-router";
import {useCbcStore} from "../stores/CbcStore.js";

export function initializeClassifiersCbcs() {
    const store = useCbcStore()
    const route = useRoute()
    if(route.params.id === undefined) return []
    store.setCbcOverClassifiers([])
    const classifiers = store.classifierNames
    const selectedCbc = store.cbcMeasurements.find(cbc => cbc.id === route.params.id)
    for(const classifier of classifiers){
        const copySelectedCbc = {...selectedCbc}
        copySelectedCbc.pred_proba = undefined
        copySelectedCbc.pred = undefined
        copySelectedCbc.confidence = undefined
        copySelectedCbc.classifier = classifier
        store.cbcOverClassifiers.push(copySelectedCbc)
    }
}