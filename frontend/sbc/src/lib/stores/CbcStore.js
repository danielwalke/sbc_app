import { defineStore } from 'pinia'
import {DEFAULT_CBC} from "../constants/CBC_Constants.js";
import { v4 as uuid } from 'uuid';
import {sortData} from "../sorting/SortData.js";
import {fetchClassifierNamesAndThresholds} from "../api/ClassifierInitialization.js";
import {getCbcMeasurements} from "../filter/CBCMeasurements.js";
import {submitCbcMeasurements} from "../api/CBCPredcitions.js";

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
		sortDirectionReversed: false,
		addTimeSeriesData: false,
		predictionType: "prospectiveRef",
		sortKeys: [],
		minSensitivity: undefined
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
		getSortDirectionReversed: (state) => state.sortDirectionReversed,
		getAddTimeSeriesData: (state) => state.addTimeSeriesData,
		getPredictionType: (state) => state.predictionType,
		getSortKeys:(state) => state.sortKeys,
		getMinSensitivity: (state) => state.minSensitivity,
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
		sortData(sortKey){
			sortData(sortKey)
		},
		setAddTimeSeriesData(val){
			this.addTimeSeriesData = val
			this.addSortKey("patientId")
		},
		async setPredictionType(val){
			this.predictionType = val
			await fetchClassifierNamesAndThresholds()
			await submitCbcMeasurements()
		},
		addSortKey(attributeName){
			const attributeNames = this.sortKeys.map(sortKey => sortKey.attributeName)
			if(attributeNames.includes(attributeName)){
				for(const sortKeyObject of this.sortKeys){
					if(sortKeyObject.attributeName === attributeName){
						sortKeyObject.ascending = !sortKeyObject.ascending
					}
				}
			}
			if(!attributeNames.includes(attributeName)){
				this.sortKeys.push({
					attributeName: attributeName,
					ascending: true
				})
			}
		},
		resetSorting(){
			this.sortKeys = []
		},
		async setMinSensitivity(minSensitivity){
			this.minSensitivity = minSensitivity
			await fetchClassifierNamesAndThresholds()
		}
	},
})
