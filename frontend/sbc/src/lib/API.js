import axios from "axios";
import {
	GRAPH_PRED_DETAILS_ENDPOINT,
	GRAPH_PRED_ENDPOINT,
	PRED_DETAILS_ENDPOINT, PRED_ENDPOINT,
	THRESHOLDS_ENDPOINT
} from "./constants/Server.js";
import {useCbcStore} from "../stores/CbcStore.js";
import {calculate_confidence_score} from "./ConfidenceCalculation.js";

function getCbcInformation(c){
	return {
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
	}
}


export function setAllPredictions(){
	const store = useCbcStore()
	store.setIsLoading(true)
	store.setHasPredictions(false)
	console.time("predictions");
	const requestDate = new Date()
	console.log(`${requestDate.getHours()}:${requestDate.getMinutes()}:${requestDate.getSeconds()}:${requestDate.getMilliseconds()}`)
	const data = store.getCbcMeasurements.map(c=> getCbcInformation(c))
	console.log(data)
	const endpoint = store.defaultClassifier === "GraphAware" ?  GRAPH_PRED_ENDPOINT : PRED_ENDPOINT
	axios.post(endpoint, {data: data, classifier: store.defaultClassifier}
	).then(function (response) {
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
}

export async function setDetailsPredictions(){
	const store = useCbcStore()
	store.setIsLoading(true)
	store.setHasPredictionDetails(false)
	console.time("details")
	const response = await axios.post(PRED_DETAILS_ENDPOINT, store.getCbcOverClassifiers.map(c=>getCbcInformation(c)))
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
}

export async function setGraphDetailsPrediction(){
	const store = useCbcStore()
	store.setIsLoading(true)
	store.setHasPredictionDetails(false)

	const allCbcMeasurements = store.$state.cbcMeasurements
	const selectedCbc = store.getCbcOverClassifiers.find(cbc => cbc.classifier === "GraphAware")
	const selectedUuid = selectedCbc.uuid
	const associatedCbcs = allCbcMeasurements.filter(cbc => cbc.patientId === selectedCbc.patientId)
	const associatedUuids = associatedCbcs.map(cbc => cbc.uuid)
	const selectedCbcIdx = associatedUuids.indexOf(selectedUuid)

	const response = await axios.post(GRAPH_PRED_DETAILS_ENDPOINT, associatedCbcs.map(c=>getCbcInformation(c)))
	store.setIsLoading(false)
	store.setHasPredictionDetails(true)
	const predDetails = response.data.prediction_details[0]

	const threshold = store.getClassifierThresholds["GraphAware"]
	selectedCbc.confidence = Math.round(calculate_confidence_score(predDetails.pred_probas[selectedCbcIdx], threshold)*10000)/100
	selectedCbc.pred_proba = predDetails.pred_probas[selectedCbcIdx]
	selectedCbc.pred = predDetails.predictions[selectedCbcIdx]? 'Sepsis' : 'Control'
	const combinedShapValues = predDetails.shap_values_list["combined"][selectedCbcIdx]
	selectedCbc.chartData = {
		labels: ["age", "sex", "HGB", "WBC", "RBC", "MCV", "PLT"],
		datasets: [{ backgroundColor: combinedShapValues.map(s => s<= 0 ? "blue" : "red"),fontColor:"white",data: combinedShapValues}]
	}
}

export async function setClassifierAndThresholds(){
	const store = useCbcStore()
	store.setIsLoading(true)
	const response = await axios.get(THRESHOLDS_ENDPOINT)
	store.setClassifierNames(Object.keys(response.data))
	store.setClassifierThresholds(response.data)
	store.setIsLoading(false)
	store.setDefaultClassifier("RandomForestClassifier")
}
