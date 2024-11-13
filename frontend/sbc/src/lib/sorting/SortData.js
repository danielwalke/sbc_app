import {useCbcStore} from "../stores/CbcStore.js";

export function sortData(sortKey){
    const store = useCbcStore()
    const cbcMeasurements= store.getCbcMeasurements
    if(store.getIsSorted === undefined){
        const uuidToIdxMapper = {}
        for(const idx in cbcMeasurements){
            const cbc = cbcMeasurements[idx]
            uuidToIdxMapper[cbc.id] = idx
        }
        store.setUuidToIdxMapper(uuidToIdxMapper)
    }
    store.setSortKey(sortKey)
    store.setSortDirectionReversed(!store.getSortDirectionReversed)
    store.setIsSorted(true)
    store.setLastSortKey(sortKey)
}

function compare( a, b, key ) {
    if ( a[key] < b[key] ){
        return -1;
    }
    if ( a[key] > b[key] ){
        return 1;
    }
    return 0;
}

export function getSortedData(state, cbcMeasurements){

    if(state.sortKey === undefined) return cbcMeasurements
    let sortedMeasurements = cbcMeasurements.sort((cbc_a, cbc_b) => compare(cbc_a, cbc_b, state.sortKey))
    if(state.lastSortKey === state.sortKey){
        if(state.sortDirectionReversed){
            sortedMeasurements = cbcMeasurements.sort((cbc_a, cbc_b) => compare(cbc_a, cbc_b, state.sortKey))
        }
        if(!state.sortDirectionReversed){
            sortedMeasurements = cbcMeasurements.sort((cbc_a, cbc_b) => compare(cbc_b, cbc_a, state.sortKey))
        }

    }
    return sortedMeasurements
}