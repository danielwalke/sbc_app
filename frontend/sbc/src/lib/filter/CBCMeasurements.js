import {useModalStore} from "../stores/ModalStore.js";
import {getSortedData} from "../sorting/SortData.js";
import {addTimeSeriesData} from "./TimeSeries.js";

export function getCbcMeasurements(state) {
    const modalStore = useModalStore()
    const noFilter = modalStore.getFilters.length === 0
    if (noFilter) return getSortedData(state, state.cbcMeasurements)

    const itemsFilters = modalStore.getFilters.filter(filter => filter["filterItems"].length > 0)
    const rangeFilters = modalStore.getFilters.filter(filter => filter["filterItems"].length === 0)
    let filteredCbcMeasurements = [...state.cbcMeasurements]
    if (itemsFilters.length > 0) {
        for (const filter of itemsFilters) {
            filteredCbcMeasurements = filteredCbcMeasurements.filter(cbc => {
                return filter["filterItems"].includes(cbc[filter["filterKey"]])
            })
        }
        // filteredCbcMeasurements = addTimeSeriesData(state, filteredCbcMeasurements)
    }
    for (const filter of rangeFilters) {
        filteredCbcMeasurements = filteredCbcMeasurements.filter(cbc => {
                const filterKey = filter["filterKey"]
                const selectedValue = filter["selectedValue"]
                const minValue = Math.floor(filter["minValue"]) //round here because slider library visualizes ints but stores floats
                const maxValue = Math.ceil(filter["maxValue"]) //round here because slider library visualizes ints but stores floats
                if (selectedValue === undefined && maxValue === undefined && minValue === undefined) return true
                if (selectedValue !== undefined) return cbc[filterKey] === selectedValue
                // if(minValue === undefined && maxValue === undefined) return filter["filterItems"].includes(cbc[filterKey])
                return (+cbc[filterKey] >= minValue && +cbc[filterKey] <= maxValue) //|| filter["filterItems"].includes(cbc[filterKey])
            }
        )
    }
    filteredCbcMeasurements = addTimeSeriesData(state, filteredCbcMeasurements)
    return getSortedData(state, filteredCbcMeasurements)
}
