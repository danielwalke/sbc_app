import { defineStore } from 'pinia'



export const useInputStore = defineStore('modal', {
	state: () => ({ cbcMeasurements: []}),
	getters: {
		getCbcMeasurements: (state) => state.cbcMeasurements,
	},
	actions: {
		addCbcMeasurements(value){
			this.cbcMeasurements.push(value)
		},
		setCbcMeasurements(value) {
			this.cbcMeasurements = value
		}
	},
})

//TODO: add watcher to cbc measurements to update filter -> cbc measurements injecten in filter modal
