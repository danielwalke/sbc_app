import { defineStore } from 'pinia'
import {DEFAULT_CBC} from "../lib/constants/CBC_Constants.js";
import axios from "axios";
import {SERVER_URL} from "../lib/constants/Server.js";


export const useCbcStore = defineStore('cbcStore', {
	state: () => ({ cbcMeasurements: [{...DEFAULT_CBC}], isLoading: false, has_predictions:false, selectedFilterValue: undefined}),
	getters: {
		getCbcMeasurements: (state) => {
			return state.cbcMeasurements
		},
		getIsLoading: (state) => state.isLoading,
		getHasPredictions: (state) => state.has_predictions,
		getSelectedFilterValue: (state) => state.selectedFilterValue,
	},
	actions: {
		addCbcMeasurements(value ){
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
						patientId: items[0],
						order: 0,
						age: +items[1],
						sex: items[2],
						HGB: Math.round(+items[3]*100)/100,
						WBC: Math.round(+items[4]*100)/100,
						RBC: Math.round(+items[5]*100)/100,
						MCV: Math.round(+items[6]*100)/100,
						PLT: Math.round(+items[7]*100)/100,
						groundTruth: items.length > 8 ? +items[8] === 1 : undefined
					})
				}
			};
			reader.readAsText(file);
		},
		submitCbcMeasurements(){
			this.isLoading = true
			this.has_predictions = false

			axios.post(SERVER_URL + 'get_pred', this.cbcMeasurements.map(c=>({
				patientId: c.patientId,
				age: c.age,
				sex: c.sex,
				HGB: c.HGB,
				WBC: c.WBC,
				RBC: c.RBC,
				MCV: c.MCV,
				PLT: c.PLT,
			})))
				.then(function (response) {
					const store = useCbcStore()
					store.setIsLoading(false)
					store.setHasPredictions(true)
					for(let i in store.getCbcMeasurements){
						const cbc = store.getCbcMeasurements[i]
						cbc.pred = response.data.predictions[i]
						cbc.pred_proba = response.data.pred_probas[i]
						cbc.chartData = {
							labels: Object.keys(cbc).filter(key =>  !["groundTruth", "pred", "pred_proba", "chartData", "order"].includes(key)).slice(1, Object.keys(cbc).length),
							datasets: [{ backgroundColor: response.data.shap_values[i].map(s => s<= 0 ? "blue" : "red"),fontColor:"white",data: response.data.shap_values[i] }]
						}
					}
				})
		},
		setSelectedFilterValue(value){
			this.selectedFilterValue = value
		}
	},
})

//TODO: add watcher to cbc measurements to update filter -> cbc measurements injecten in filter modal
