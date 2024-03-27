import { defineStore } from 'pinia'
import {DEFAULT_CBC, PREDICTION_THRESHOLD} from "../lib/constants/CBC_Constants.js";
import axios from "axios";
import {
	GRAPH_PRED_DETAILS_ENDPOINT, GRAPH_PRED_ENDPOINT,
	PRED_DETAILS_ENDPOINT,
	PRED_ENDPOINT,
	SERVER_URL,
	THRESHOLDS_ENDPOINT
} from "../lib/constants/Server.js";
import {useModalStore} from "./ModalStore.js";
import { v4 as uuid } from 'uuid';
import {useRoute} from "vue-router";
import {saveAs} from "file-saver";

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
	state: () => ({ cbcMeasurements: [{...DEFAULT_CBC, id : uuid()}], isLoading: false, has_predictions:false,
		cbcOverClassifiers: [], classifierNames: [], classifierThresholds: undefined, hasPredictionDetails: false,
		defaultClassifier: "RandomForestClassifier", auroc: undefined}),
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
		getHasPredictionDetails: (state) => state.hasPredictionDetails,
		getAuroc: (state) => {
			const groundTruthList = state.getCbcMeasurements.map(cbc => cbc.groundTruth)
			if(groundTruthList.some(y => y === undefined)) return "Calculation without ground-truth not possible"
			if(new Set(groundTruthList).size === 1) return "Calculation for only one label not possible"
			return Math.round(state.auroc * 10000) / 10000
		}
	},
	actions: {
		addCbcMeasurements(value ){
			value.id = uuid()
			this.has_predictions = false
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
		setAuroc(value){
			this.auroc = value
		},
		readCbcFile(file){
			const reader = new FileReader();
			let content = null;
			reader.onload = (res) => {
				this.cbcMeasurements = []
				this.has_predictions = false
				content = res.target.result;
				const lines = content.split("\n")
				for(const lineIdx in lines){
					const line = lines[lineIdx]
					if(line.length===0 || lineIdx==0) continue
					const items = line.split(";")
					this.addCbcMeasurements({
						uuid: uuid(),
						patientId: items[0],
						order: +items[1],
						age: +items[2],
						sex: items[3],
						HGB: Math.round(+items[4]*100)/100,
						WBC: Math.round(+items[5]*100)/100,
						RBC: Math.round(+items[6]*100)/100,
						MCV: Math.round(+items[7]*100)/100,
						PLT: Math.round(+items[8]*100)/100,
						groundTruth: items.length > 8 ? +items[9] === 1 ? 'Sepsis' : 'Control' : undefined
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
			const data = store.getCbcMeasurements.map(c=>({
				id: c.patientId,
				order: c.order,
				age: c.age,
				sex: c.sex,
				HGB: c.HGB,
				WBC: c.WBC,
				RBC: c.RBC,
				MCV: c.MCV,
				PLT: c.PLT,
				ground_truth: c.groundTruth === "Sepsis" ? 1 : c.groundTruth === "Control"? 0: undefined,
			}))
			console.log(data)
			const endpoint = store.defaultClassifier === "GraphAware" ?  GRAPH_PRED_ENDPOINT : PRED_ENDPOINT
			axios.post(endpoint, {data: data, classifier: store.defaultClassifier}
			).then(function (response) {
					console.log(response)
					store.setIsLoading(false)
					store.setHasPredictions(true)
					for(let i in store.getCbcMeasurements){
						const cbc = store.getCbcMeasurements[i]
						cbc.pred = response.data.predictions[i] ? 'Sepsis' : 'Control'
						cbc.pred_proba = response.data.pred_probas[i]
						const threshold = store.getClassifierThresholds[store.defaultClassifier]
						cbc.confidence = Math.round(calculate_confidence_score(cbc.pred_proba, threshold)*10000)/100
					}
					store.setAuroc(response.data.auroc)
					console.timeEnd("predictions");
				})
		},
		setHasPredictionDetails(value){
			this.hasPredictionDetails = value
		},
		async submitCbcMeasurementDetails(){
			const store = useCbcStore()
			store.setIsLoading(true)
			store.setHasPredictionDetails(false)
			console.time("details")
			const response = await axios.post(PRED_DETAILS_ENDPOINT, store.getCbcOverClassifiers.map(c=>({
				age: c.age,
				sex: c.sex,
				HGB: c.HGB,
				WBC: c.WBC,
				RBC: c.RBC,
				MCV: c.MCV,
				PLT: c.PLT,
			})))
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
			await store.setGraphAwarePrediction()
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
			const response = await axios.get(THRESHOLDS_ENDPOINT)
			store.setClassifierNames(Object.keys(response.data))
			store.setClassifierThresholds(response.data)
			store.setIsLoading(false)
		},
		async setGraphAwarePrediction(){
			const store = useCbcStore()
			store.setIsLoading(true)
			store.setHasPredictionDetails(false)

			const allCbcMeasurements = store.$state.cbcMeasurements
			const selectedCbc = store.getCbcOverClassifiers.find(cbc => cbc.classifier === "GraphAware")
			const selectedUuid = selectedCbc.uuid
			console.log(allCbcMeasurements)
			console.log(allCbcMeasurements.length)
			const associatedCbcs = allCbcMeasurements.filter(cbc => cbc.patientId === selectedCbc.patientId)
			console.log(associatedCbcs)
			const associatedUuids = associatedCbcs.map(cbc => cbc.uuid)
			console.log(associatedUuids)
			const selectedCbcIdx = associatedUuids.indexOf(selectedUuid)
			console.log("Index is: ")
			console.log(selectedCbcIdx)
			console.log("UUid is: ")
			console.log(selectedUuid)

			const response = await axios.post(GRAPH_PRED_DETAILS_ENDPOINT, associatedCbcs.map(c=>({
				id: c.patientId,
				order: c.order,
				age: c.age,
				sex: c.sex,
				HGB: c.HGB,
				WBC: c.WBC,
				RBC: c.RBC,
				MCV: c.MCV,
				PLT: c.PLT
			})))
			store.setIsLoading(false)
			store.setHasPredictionDetails(true)
			const predDetails = response.data.prediction_details[0]
			console.log(predDetails)

			const threshold = store.getClassifierThresholds["GraphAware"]
			selectedCbc.confidence = Math.round(calculate_confidence_score(predDetails.pred_probas[selectedCbcIdx], threshold)*10000)/100
			selectedCbc.pred_proba = predDetails.pred_probas[selectedCbcIdx]
			selectedCbc.pred = predDetails.predictions[selectedCbcIdx]? 'Sepsis' : 'Control'
			const combinedShapValues = predDetails.shap_values_list["combined"][selectedCbcIdx]
			selectedCbc.chartData = {
				labels: ["age", "sex", "HGB", "WBC", "RBC", "MCV", "PLT"],
				datasets: [{ backgroundColor: combinedShapValues.map(s => s<= 0 ? "blue" : "red"),fontColor:"white",data: combinedShapValues}]
			}
			console.log(selectedCbc)
		},
		setDefaultClassifier(newSelectedValue){
			this.defaultClassifier = newSelectedValue
		},
		checkAUROCForDefaultClassifier(){

		},
		download(){
			const store = useCbcStore()
			const cbcs = store.getCbcMeasurements
			let output = ""
			if(cbcs.length < 1) return console.alert("Provide enough data")
			const keys = Object.keys(cbcs[0])
			output += keys.join(";")
			output += "\n"
			for(const cbc of cbcs){
				output += Object.values(cbc).join(";")
				output += "\n"
			}

			const blob =  new Blob(new Array(output.trim()), {type: "text/plain;charset=utf-8"});
			saveAs(blob, "ModuleGraph.csv")
		}
	},
})
