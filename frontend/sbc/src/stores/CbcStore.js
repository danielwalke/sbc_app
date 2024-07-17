import { defineStore } from 'pinia'
import {DEFAULT_CBC, PREDICTION_THRESHOLD} from "../lib/constants/CBC_Constants.js";
import axios from "axios";
import {SERVER_URL} from "../lib/constants/Server.js";
import {useModalStore} from "./ModalStore.js";
import { v4 as uuid } from 'uuid';
import {useRoute} from "vue-router";

function calculate_confidence_score(class_probability, threshold = 0.5){
	let m
	let n
	if(class_probability <= threshold){
		m = 0.5 / threshold
		n = 0
	}else{
		m = 0.5 / (1- threshold)
		n = 0.5 - m * threshold
	}
	const confidence = m*class_probability+n
	return confidence
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


function getSortedData(state, cbcMeasurements){

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

function addTimeSeriesData(state, filteredCbcMeasurements){
	if(!state.addTimeSeriesData) return filteredCbcMeasurements
	const filteredPatientIds = filteredCbcMeasurements.map(cbc => cbc.patientId)
	const filteredUuids = filteredCbcMeasurements.map(cbc => cbc.id)
	const timeSeriesData = state.cbcMeasurements.filter(cbc => filteredPatientIds.includes(cbc.patientId) && !filteredUuids.includes(cbc.id))
	filteredCbcMeasurements.push(...timeSeriesData)
	return filteredCbcMeasurements
}

export const useCbcStore = defineStore('cbcStore', {
	state: () => ({ cbcMeasurements: [{...DEFAULT_CBC, id : uuid()}], isLoading: false, has_predictions:false, cbcOverClassifiers: [], classifierNames: [], classifierThresholds: undefined, hasPredictionDetails: false, isSorted: undefined, uuidToIdxMapper:undefined, lastSortKey: undefined, sortDirectionReversed: false, addTimeSeriesData: false, sortKey:undefined }),
	getters: {
		getCbcMeasurements: (state) => {
			const modalStore = useModalStore()
			const noFilter = modalStore.getFilters.length === 0
			if(noFilter) return getSortedData(state, state.cbcMeasurements)
			const itemsFilters = modalStore.getFilters.filter(filter => filter["filterItems"].length > 0)
			const rangeFilters = modalStore.getFilters.filter(filter => filter["filterItems"].length === 0)

			let filteredCbcMeasurements = [...state.cbcMeasurements]
			if(itemsFilters.length > 0){
				for(const filter of itemsFilters){
					filteredCbcMeasurements = filteredCbcMeasurements.filter(cbc => {
						return filter["filterItems"].includes(cbc[filter["filterKey"]])
					})
				}
				filteredCbcMeasurements = addTimeSeriesData(state, filteredCbcMeasurements)

				// return getSortedData(state, filteredCbcMeasurements)
			}
			for(const filter of rangeFilters){
				filteredCbcMeasurements = filteredCbcMeasurements.filter(cbc => {
						const filterKey = filter["filterKey"]
						const selectedValue = filter["selectedValue"]
						const minValue = Math.round(filter["minValue"]) //round here because slider library visualizes ints but stores floats
						const maxValue = Math.round(filter["maxValue"]) //round here because slider library visualizes ints but stores floats
						if(selectedValue === undefined && maxValue === undefined && minValue === undefined) return true
						if (selectedValue !== undefined) return cbc[filterKey] === selectedValue
						// if(minValue === undefined && maxValue === undefined) return filter["filterItems"].includes(cbc[filterKey])
						return (+cbc[filterKey] >= minValue && +cbc[filterKey] <= maxValue) //|| filter["filterItems"].includes(cbc[filterKey])
					}
				)
			}
			filteredCbcMeasurements = addTimeSeriesData(state, filteredCbcMeasurements)

			return getSortedData(state, filteredCbcMeasurements)
		},
		getUnfilteredCbcMeasurements: (state) => state.cbcMeasurements,
		getIsLoading: (state) => state.isLoading,
		getHasPredictions: (state) => state.has_predictions,
		getCbcOverClassifiers: (state) => {
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
		},
		getClassifierThresholds: (state) => state.classifierThresholds,
		getHasPredictionDetails: (state) => state.hasPredictionDetails,
		getIsSorted: (state) => state.isSorted,
		getUuidToIdxMapper: (state) => state.uuidToIdxMapper,
		getLastSortKey: (state) => state.lastSortKey,
		getSortDirectionReversed: (state) => state.sortDirectionReversed,
		getAddTimeSeriesData: (state) => state.addTimeSeriesData

	},
	actions: {
		addCbcMeasurements(value ){
			value.id = uuid()
			this.cbcMeasurements.push(value)
		},
		unshiftCbcMeasurements(value ){
			value.id = uuid()
			this.cbcMeasurements.unshift(value)
		},
		setCbcMeasurements(value) {
			this.cbcMeasurements = value
		},
		setIsLoading(value){
			this.isLoading = value
		},
		setHasPredictions(value){
			this.has_predictions = value
		},
		parseFile(content){
			this.has_predictions = false
			const filterStore = useModalStore()
			filterStore.setFilters([])
			const lines = content.split("\n")
			for(const lineIdx in lines){
				const line = lines[lineIdx]
				if(line.length===0 || lineIdx==0) continue
				const items = line.split(";")
				this.addCbcMeasurements({
					id: uuid(),
					patientId: items[0],
					order: +items[1],
					age: +items[2],
					sex: items[3],
					HGB: Math.round(+items[4]*100)/100,
					WBC: Math.round(+items[5]*100)/100,
					RBC: Math.round(+items[6]*100)/100,
					MCV: Math.round(+items[7]*100)/100,
					PLT: Math.round(+items[8]*100)/100,
					groundTruth: items.length > 9 ? +items[9] === 1 ? 'Sepsis' : 'Control' : undefined
				})
			}
		},
		readCbcFile(file){
			const reader = new FileReader();
			let content = null;
			reader.onload = (res) => {
				// this.cbcMeasurements = []
				content = res.target.result;
				this.parseFile(content)
			};
			reader.readAsText(file);
		},
		async submitCbcMeasurements(){
			const modalStore = useModalStore()
			modalStore.setFilters(modalStore.getFilters.filter(filter => !["confidence"].includes(filter["filterKey"])))
			const store = useCbcStore()
			store.setIsLoading(true)
			store.setHasPredictions(false)
			const requestDate = new Date()
			console.log(`${requestDate.getHours()}:${requestDate.getMinutes()}:${requestDate.getSeconds()}:${requestDate.getMilliseconds()}`)
			axios.post(SERVER_URL + 'get_pred', store.getCbcMeasurements.map(c=>({
				age: c.age,
				sex: c.sex,
				HGB: c.HGB,
				WBC: c.WBC,
				RBC: c.RBC,
				MCV: c.MCV,
				PLT: c.PLT,
			})))
				.then(function (response) {
					store.setIsLoading(false)
					store.setHasPredictions(true)
					for(let i in store.getCbcMeasurements){
						const cbc = store.getCbcMeasurements[i]
						cbc.pred = response.data.predictions[i] ? 'Sepsis' : 'Control'
						cbc.pred_proba = response.data.pred_probas[i]
						const threshold = store.getClassifierThresholds["RandomForestClassifier"]
						cbc.confidence = Math.round(calculate_confidence_score(cbc.pred_proba, threshold)*10000)/100
					}
					console.timeEnd("predictions");
				})
				.then(()=>{
					const cbcsWithDetails = store.getCbcMeasurements.filter(cbc => cbc.chartData)
					for(const cbc of cbcsWithDetails){
						this.submitCbcDetail(cbc)
					}
				})
		},
		setHasPredictionDetails(value){
			this.hasPredictionDetails = value
		},
		submitCbcMeasurementDetails(){
			const store = useCbcStore()
			store.setIsLoading(true)
			store.setHasPredictionDetails(false)
			console.time("details")
			axios.post(SERVER_URL + 'get_pred_details', store.getCbcOverClassifiers.map(c=>({
				age: c.age,
				sex: c.sex,
				HGB: c.HGB,
				WBC: c.WBC,
				RBC: c.RBC,
				MCV: c.MCV,
				PLT: c.PLT,
			})))
				.then(function (response) {
					store.setIsLoading(false)
					store.setHasPredictionDetails(true)
					for(let i in response.data.prediction_details){
						const cbc = store.getCbcOverClassifiers[i]
						const prediction_detail = response.data.prediction_details[i]
						cbc.pred = prediction_detail.prediction ? 'Sepsis' : 'Control'
						cbc.classifier = prediction_detail.classifier_name
						cbc.pred_proba = prediction_detail.pred_proba
						const threshold = store.getClassifierThresholds[cbc.classifier]
						cbc.confidence = Math.round(calculate_confidence_score(cbc.pred_proba, threshold)*10000)/100
						cbc.chartData = {
							labels: ["age", "sex", "HGB", "WBC", "RBC", "MCV", "PLT"],
							datasets: [{ backgroundColor: prediction_detail.shap_values.map(s => s<= 0 ? "#2563eb" : "#dc2626"),fontColor:"white",data: prediction_detail.shap_values}]
						}
					}
					console.timeEnd("details")
				})
		},
		setClassifierNames(classifierNames){
			this.classifierNames = classifierNames
		},
		setClassifierThresholds(classifierThresholds){
			this.classifierThresholds = classifierThresholds
		},
		async fetchClassifierNames(){
			const store = useCbcStore()
			store.setIsLoading(true)
			const response = await axios.get(SERVER_URL + 'classifier_thresholds')
			store.setClassifierNames(Object.keys(response.data))
			store.setClassifierThresholds(response.data)
			store.setIsLoading(false)
		},
		setCbcOverClassifiers(newCbcOverClassifiers){
			this.cbcOverClassifiers =newCbcOverClassifiers
		},
		submitCbcDetail(cbc){
			const store = useCbcStore()
			store.setIsLoading(true)
			axios.post(SERVER_URL + 'get_pred_detail', cbc)
				.then(function (response) {
					store.setIsLoading(false)
					for(let i in response.data.prediction_details){
						const prediction_detail = response.data.prediction_details[0]
						cbc.pred = prediction_detail.prediction ? 'Sepsis' : 'Control'
						cbc.classifier = prediction_detail.classifier_name
						cbc.pred_proba = prediction_detail.pred_proba
						const threshold = store.getClassifierThresholds[cbc.classifier]
						cbc.confidence = Math.round(calculate_confidence_score(cbc.pred_proba, threshold)*10000)/100
						cbc.chartData = {
							labels: ["age", "sex", "HGB", "WBC", "RBC", "MCV", "PLT"],
							datasets: [{ backgroundColor: prediction_detail.shap_values.map(s => s<= 0 ? "#2563eb" : "#dc2626"),fontColor:"white",data: prediction_detail.shap_values}]
						}
					}
				})
		},
		setIsSorted(value){
			this.isSorted = value
		},
		setUuidToIdxMapper(value){
			this.uuidToIdxMapper = value
		},
		setLastSortKey(value){
			this.lastSortKey = value
		},
		setSortDirectionReversed(value){
			this.sortDirectionReversed = value
		},
		setSortKey(val){
			this.sortKey = val
 		},
		sortData(sortKey){
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
		},
		resetSort(){
			const store = useCbcStore()
			store.setIsSorted(false)
		},
		setAddTimeSeriesData(val){
			this.addTimeSeriesData = val
			this.sortKey = "patientId"
		}
	},
})
