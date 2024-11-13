import { defineStore } from 'pinia'
import {DEFAULT_CBC} from "../constants/CBC_Constants.js";
import { v4 as uuid } from 'uuid';
import {sortData} from "../sorting/SortData.js";
import {fetchClassifierNamesAndThresholds} from "../api/ClassifierInitialization.js";
import {getCbcMeasurements} from "../filter/CBCMeasurements.js";

export const useCbcStore = defineStore('cbcStore', {
	state: () => ({
		cbcMeasurements: [{...DEFAULT_CBC, id : uuid()}],
		isLoading: false,
		has_predictions:false,
		cbcOverClassifiers: [],
		classifierNames: [],
		classifierThresholds: undefined,
		hasPredictionDetails: false,
		isSorted: undefined,
		uuidToIdxMapper:undefined,
		lastSortKey: undefined,
		sortDirectionReversed: false,
		addTimeSeriesData: false,
		sortKey:undefined,
		predictionType: "prospective"
	}),
	getters: {
		getCbcMeasurements: (state) => getCbcMeasurements(state),
		getUnfilteredCbcMeasurements: (state) => state.cbcMeasurements,
		getIsLoading: (state) => state.isLoading,
		getHasPredictions: (state) => state.has_predictions,
		getCbcOverClassifiers: (state) =>  state.cbcOverClassifiers,
		getClassifierThresholds: (state) => state.classifierThresholds,
		getHasPredictionDetails: (state) => state.hasPredictionDetails,
		getIsSorted: (state) => state.isSorted,
		getUuidToIdxMapper: (state) => state.uuidToIdxMapper,
		getLastSortKey: (state) => state.lastSortKey,
		getSortDirectionReversed: (state) => state.sortDirectionReversed,
		getAddTimeSeriesData: (state) => state.addTimeSeriesData,
		getPredictionType: (state) => state.predictionType
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
		setHasPredictionDetails(value){
			this.hasPredictionDetails = value
		},
		setClassifierNames(classifierNames){
			this.classifierNames = classifierNames
		},
		setClassifierThresholds(classifierThresholds){
			this.classifierThresholds = classifierThresholds
		},
		setCbcOverClassifiers(newCbcOverClassifiers){
			this.cbcOverClassifiers =newCbcOverClassifiers
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
			sortData(sortKey)
		},
		setAddTimeSeriesData(val){
			this.addTimeSeriesData = val
			this.sortKey = "patientId"
		},
		async setPredictionType(val){
			this.predictionType = val
			await fetchClassifierNamesAndThresholds()
		}
	},
})
