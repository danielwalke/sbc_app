import {useCbcStore} from "../stores/CbcStore.js";

export function sortData(sortKey){
    const store = useCbcStore()
    store.addSortKey(sortKey)
}

function compare( a, b, keys) {
    for(const key of keys){
        if ( a[key.attributeName] < b[key.attributeName] && key.ascending){
            return -1;
        }
        if ( a[key.attributeName] < b[key.attributeName] && !key.ascending){
            return 1;
        }
        if ( a[key.attributeName] > b[key.attributeName] && key.ascending){
            return 1;
        }
        if ( a[key.attributeName] > b[key.attributeName] && !key.ascending){
            return -1;
        }
    }
    return 0;
}

export function getSortedData(state, cbcMeasurements){
    return cbcMeasurements.sort((cbc_a, cbc_b) => compare(cbc_b, cbc_a, state.sortKeys))
}