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
		m = - 1 / threshold
		n = 1
	}else{
		m = 1 / (1-threshold)
		n = - threshold * m
	}
	const confidence = m*class_probability+n
	return confidence
}


export const useCbcStore = defineStore('cbcStore', {
	state: () => ({ cbcMeasurements: [{...DEFAULT_CBC, id : uuid()}], isLoading: false, has_predictions:false, cbcOverClassifiers: [], classifierNames: [], classifierThresholds: undefined, hasPredictionDetails: false}),
	getters: {
		getCbcMeasurements: (state) => {
			const modalStore = useModalStore()
			const filterKey = modalStore.getFilterKey
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
		getHasPredictionDetails: (state) => state.hasPredictionDetails
	},
	actions: {
		addCbcMeasurements(value ){
			value.id = uuid()
			this.cbcMeasurements.push(value)
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
		readCbcFile(file){
			const reader = new FileReader();
			let content = null;
			reader.onload = (res) => {
				this.cbcMeasurements = []
				content = res.target.result;
				const lines = content.split("\n")
				for(const lineIdx in lines){
					const line = lines[lineIdx]
					if(line.length===0 || lineIdx==0) continue
					const items = line.split(";")
					this.addCbcMeasurements({
						id: uuid(),
						patientId: items[0],
						order: 0,
						age: +items[1],
						sex: items[2],
						HGB: Math.round(+items[3]*100)/100,
						WBC: Math.round(+items[4]*100)/100,
						RBC: Math.round(+items[5]*100)/100,
						MCV: Math.round(+items[6]*100)/100,
						PLT: Math.round(+items[7]*100)/100,
						groundTruth: items.length > 8 ? +items[8] === 1 ? 'Sepsis' : 'Control' : undefined
					})
				}
			};
			reader.readAsText(file);
		},
		submitCbcMeasurements(){
			const store = useCbcStore()
			store.setIsLoading(true)
			store.setHasPredictions(false)
			console.time("predictions");
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
							datasets: [{ backgroundColor: prediction_detail.shap_values.map(s => s<= 0 ? "blue" : "red"),fontColor:"white",data: prediction_detail.shap_values}]
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
		}
	},
})
