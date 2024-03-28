import {defineStore} from 'pinia'
import {DEFAULT_CBC} from "../lib/constants/CBC_Constants.js";
import {v4 as uuid} from 'uuid';
import {readCSV} from "../lib/InputReader.js";
import {exportCSV} from "../lib/Exporter.js";
import {
	setAllPredictions,
	setClassifierAndThresholds,
	setDetailsPredictions,
	setGraphDetailsPrediction
} from "../lib/API.js";
import {getAUROCOutput} from "../lib/AUROC.js";
import {getCbcForEachClassifier, getFilteredCbcMeasurements} from "../lib/CBCMeasurements.js";

export const useCbcStore = defineStore('cbcStore', {
	state: () => ({
		cbcMeasurements: [{...DEFAULT_CBC, id: uuid()}],
		isLoading: false,
		has_predictions: false,
		cbcOverClassifiers: [],
		classifierNames: [],
		classifierThresholds: undefined,
		hasPredictionDetails: false,
		defaultClassifier: "RandomForestClassifier",
		auroc: undefined
	}),
	getters: {
		getCbcMeasurements: (state) => {
			return getFilteredCbcMeasurements(state)
		},
		getUnfilteredCbcMeasurements: (state) => state.cbcMeasurements,
		getIsLoading: (state) => state.isLoading,
		getHasPredictions: (state) => state.has_predictions,
		getCbcOverClassifiers: (state) => {
			return getCbcForEachClassifier(state)
		},
		getClassifierThresholds: (state) => state.classifierThresholds,
		getHasPredictionDetails: (state) => state.hasPredictionDetails,
		getAuroc: (state) => getAUROCOutput(state)

	},
	actions: {
		addCbcMeasurements(value) {
			value.id = uuid()
			this.has_predictions = false
			this.cbcMeasurements.push(value)
		},
		setCbcMeasurements(value) {
			this.cbcMeasurements = value
		},
		setIsLoading(value) {
			this.isLoading = value
		},
		setHasPredictions(value) {
			this.has_predictions = value
		},
		setAuroc(value) {
			this.auroc = value
		},
		readCbcFile(file) {
			readCSV(file)
		},
		submitCbcMeasurements() {
			setAllPredictions()
		},
		setHasPredictionDetails(value) {
			this.hasPredictionDetails = value
		},
		async submitCbcMeasurementDetails() {
			await setDetailsPredictions()
		},
		setClassifierNames(classifierNames) {
			this.classifierNames = classifierNames
		},
		setClassifierThresholds(classifierThresholds) {
			this.classifierThresholds = classifierThresholds
		},
		async fetchClassifierNames() {
			await setClassifierAndThresholds()
		},
		async setGraphAwarePrediction() {
			await setGraphDetailsPrediction()
		},
		setDefaultClassifier(newSelectedValue) {
			this.defaultClassifier = newSelectedValue
		},
		download() {
			exportCSV()
		}
	},
})
