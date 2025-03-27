import { defineStore } from 'pinia'
import {useCbcStore} from "./CbcStore.js";

export const useModalStore = defineStore('modal', {
	state: () => ({
		isHelpModalOpen: false,
		headerContent: undefined,
		helpMainContent: undefined,
		isFilterModalOpen: false,
		filterKey: undefined,
		filters: [],
		isInputModelOpen: false,
		isSensitivityModelOpen: false,
		isScrolled: false
	}),
	getters: {
		getHeaderContent: (state) => state.headerContent,
		getHelpMainContent: (state) => state.helpMainContent,
		getIsHelpModalOpen: (state) => state.isHelpModalOpen,
		getIsFilterModalOpen: (state) => state.isFilterModalOpen,
		getFilterOptions: (state) =>{
			const cbcStore = useCbcStore()
			const definedFilterMeasurements = cbcStore.getCbcMeasurements.filter( cbc => cbc[state.filterKey] !== undefined)
			const options = definedFilterMeasurements.map(cbc => cbc[state.filterKey])
			const uniqueOptions = Array.from(new Set(options))
			return uniqueOptions.map(option => ({
				value: option,
				name: option
			}))
		},
		getAllFilterOptions: (state) =>{
			const cbcStore = useCbcStore()
			const definedFilterMeasurements = cbcStore.getUnfilteredCbcMeasurements.filter( cbc => cbc[state.filterKey] !== undefined)
			const options = definedFilterMeasurements.map(cbc => cbc[state.filterKey])
			const uniqueOptions = Array.from(new Set(options))
			return uniqueOptions.map(option => ({
				value: option,
				name: option
			}))
		},
		getFilterKey: (state) => state.filterKey,
		getFilters: (state) => state.filters,
		getSelectedItemsFromFilter: (state) => {
			let filter = state.getFilters.find(filter => filter["filterKey"] === state.getFilterKey)
			if(filter === undefined) return []
			return filter["filterItems"]
		},
		getIsInputModelOpen: (state) => state.isInputModelOpen,
		getIsSensitivityModelOpen: (state) => state.isSensitivityModelOpen,
		getIsScrolled: (state)=> state.isScrolled
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
		setIsInputModalOpen(value) {
			this.isInputModelOpen = value
		},
		setFilterKey(value){
			this.filterKey = value
		},
		addFilter(filter){
			this.filters.push(filter)
		},
		setFilters(value){
			this.filters = value
		},
		addSelectedItemToFilter(item){
			let filter = this.getFilters.find(filter => filter["filterKey"] === this.getFilterKey)
			if(filter === undefined) {
				filter = {
					filterKey: this.getFilterKey,
					selectedValue: undefined,
					minValue: undefined,
					maxValue: undefined,
					filterItems: [item]
				}
				return this.filters.push(filter)
			}
			filter["filterItems"].push(item)
		},
		removeItemFromFilter(itemToDelete){
			let filter = this.getFilters.find(filter => filter["filterKey"] === this.getFilterKey)
			filter["filterItems"] = filter["filterItems"].filter(item => item !== itemToDelete)
			if(filter["filterItems"].length === 0){
				this.filters = this.filters.filter(f => f["filterKey"] !== filter["filterKey"])
			}
		},
		setIsSensitivityModelOpen(isOpen){
			this.isSensitivityModelOpen = isOpen
		},
		setIsScrolled(isScrolled){
			this.isScrolled = isScrolled
		}
	},
})
