import { defineStore } from 'pinia'



export const useModalStore = defineStore('modal', {
	state: () => ({ isOpen: false, headerContent: undefined, mainContent: undefined }),
	getters: {
		getHeaderContent: (state) => state.headerContent,
		getMainContent: (state) => state.mainContent,
		getIsOpen: (state) => state.isOpen,
	},
	actions: {
		setIsOpen(value){
			this.isOpen = value
		},
		setHeaderContent(value) {
			this.headerContent = value
		},
		setMainContent(value) {
			this.mainContent = value
		},
	},
})
