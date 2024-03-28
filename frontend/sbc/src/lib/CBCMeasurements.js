import {useModalStore} from "../stores/ModalStore.js";
import {useRoute} from "vue-router";

export function getFilteredCbcMeasurements(state){
	const modalStore = useModalStore()
	const noFilter = modalStore.getFilters.length === 0
	if(noFilter) return state.cbcMeasurements
	let filteredCbcMeasurements = [...state.cbcMeasurements]
	for(const filter of modalStore.getFilters){
		filteredCbcMeasurements = filteredCbcMeasurements.filter(cbc => {
				const filterKey = filter["filterKey"]
				const selectedValue = filter["selectedValue"]
				const minValue = filter["minValue"]
				const maxValue = filter["maxValue"]
				if (selectedValue !== undefined) return cbc[filterKey] === selectedValue
				return +cbc[filterKey] >= minValue && +cbc[filterKey] <= maxValue
			}
		)
	}
	return filteredCbcMeasurements
}


export function getCbcForEachClassifier(state){
	const route = useRoute()
	if(route.params.id === undefined) return []
	const classifiers = state.classifierNames
	const cbcOverClassifiers = []
	const selectedCbc = state.cbcMeasurements.find(cbc => cbc.id === route.params.id)
	for(const classifier of classifiers){
		const copySelectedCbc = {...selectedCbc}
		copySelectedCbc.pred_proba = undefined
		copySelectedCbc.pred = undefined
		copySelectedCbc.confidence = undefined
		copySelectedCbc.classifier = classifier
		cbcOverClassifiers.push(copySelectedCbc)
	}
	return cbcOverClassifiers
}
