import { defineStore } from 'pinia'
import {useCbcStore} from "./CbcStore.js";



export const useModalStore = defineStore('modal', {
	state: () => ({ isHelpModalOpen: false, headerContent: undefined, helpMainContent: undefined,
	isFilterModalOpen: false, filterKey: undefined, filters: []}),
	getters: {
		getHeaderContent: (state) => state.headerContent,
		getHelpMainContent: (state) => state.helpMainContent,
		getIsHelpModalOpen: (state) => state.isHelpModalOpen,
		getIsFilterModalOpen: (state) => state.isFilterModalOpen,
		getFilterOptions: (state) =>{
			const cbcStore = useCbcStore()
			const options = cbcStore.getCbcMeasurements.map(cbc => cbc[state.filterKey])
			const uniqueOptions = Array.from(new Set(options))
			return uniqueOptions.map(option => ({
				value: option,
				name: option
			}))
		},
		getAllFilterOptions: (state) =>{
			const cbcStore = useCbcStore()
			const options = cbcStore.getUnfilteredCbcMeasurements.map(cbc => cbc[state.filterKey])
			const uniqueOptions = Array.from(new Set(options))
			return uniqueOptions.map(option => ({
				value: option,
				name: option
			}))
		},
		getFilterKey: (state) => state.filterKey,
		getFilters: (state) => state.filters
	},
	actions: {
		setIsHelpModalOpen(value){
			this.isHelpModalOpen = value
		},
		setHeaderContent(value) {
			this.headerContent = value
		},
		setHelpMainContent(value) {
			this.helpMainContent = value
		},
		setIsFilterModalOpen(value) {
			this.isFilterModalOpen = value
		},
		setFilterKey(value){
			this.filterKey = value
		},
		addFilter(filter){
			this.filters.push(filter)
		},
		setFilter(value){
			this.filters = value
		}
	},
})
