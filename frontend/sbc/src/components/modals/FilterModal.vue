<template>
	<div :class="isOpen ? 'block' : 'hidden' " id="default-modal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-2
	 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
		<div class="relative p-4 w-full max-w-2xl max-h-full">
			<!-- Modal content -->
			<div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
				<!-- Modal header -->
				<div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
					<h3 class="text-xl font-semibold text-gray-900 dark:text-white">
						{{headerContent}}
					</h3>
					<button @click="close" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="default-modal">
						<svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
							<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
						</svg>
						<span class="sr-only">Close modal</span>
					</button>
				</div>
				<!-- Modal body -->
				<div class="p-4 md:p-5 space-y-4">
					<div v-if="isCategorical">
						<form class="max-w-sm mx-auto">
							<select v-model="selectedValue" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
								<option type="button"  :value="undefined">Select All</option>
								<option type="button"  v-for="option in allFilterOptions"  :value="option.value">{{option.name}}</option>
							</select>
						</form>
					</div>
					<div v-else>
						<Slider v-model="rangeValues" :min="defaultRangeValues()[0]" :max="defaultRangeValues()[1]" :classes="{
  target: 'relative box-border select-none touch-none tap-highlight-transparent touch-callout-none disabled:cursor-not-allowed',
  focused: 'slider-focused',
  tooltipFocus: 'slider-tooltip-focus',
  tooltipDrag: 'slider-tooltip-drag',
  ltr: 'slider-ltr',
  rtl: 'slider-rtl',
  horizontal: 'slider-horizontal h-1.5',
  textDirectionRtl: 'slider-txt-rtl',
  textDirectionLtr: 'slider-txt-ltr',
  base: 'w-full h-full relative z-1 bg-gray-300 rounded',
  connects: 'w-full h-full relative overflow-hidden z-0 rounded',
  connect: 'absolute z-1 top-0 right-0 transform-origin-0 transform-style-flat h-full w-full bg-sky-700 cursor-pointer tap:duration-300 tap:transition-transform disabled:bg-gray-400 disabled:cursor-not-allowed',
  origin: 'slider-origin absolute z-1 top-0 right-0 transform-origin-0 transform-style-flat h-full w-full h:h-0 v:-top-full txt-rtl-h:left-0 txt-rtl-h:right-auto v:w-0 tap:duration-300 tap:transition-transform',
  handle: 'absolute rounded-full bg-white border-0 shadow-slider cursor-grab focus:outline-none h:w-4 h:h-4 h:-top-1.5 h:-right-2 txt-rtl-h:-left-2 txt-rtl-h:right-auto v:w-4 v:h-4 v:-top-2 v:-right-1.25 disabled:cursor-not-allowed focus:ring focus:ring-sky-700 focus:ring-opacity-30',
  handleLower: 'slider-hande-lower',
  handleUpper: 'slider-hande-upper',
  touchArea: 'h-full w-full',
  tooltip: 'absolute block text-sm font-semibold whitespace-nowrap py-1 px-1.5 min-w-5 text-center text-white rounded border border-sky-700 bg-sky-700 transform h:-translate-x-1/2 h:left-1/2 v:-translate-y-1/2 v:top-1/2 disabled:bg-gray-400 disabled:border-gray-400 merge-h:translate-x-1/2 merge-h:left-auto merge-v:-translate-x-4 merge-v:top-auto tt-focus:hidden tt-focused:block tt-drag:hidden tt-dragging:block',
  tooltipTop: 'bottom-6 h:arrow-bottom merge-h:bottom-3.5',
  tooltipBottom: 'top-6 h:arrow-top merge-h:top-5',
  tooltipLeft: 'right-6 v:arrow-right merge-v:right-1',
  tooltipRight: 'left-6 v:arrow-left merge-v:left-7',
  tooltipHidden: 'slider-tooltip-hidden',
  active: 'slider-active shadow-slider-active cursor-grabbing',
  draggable: 'cursor-ew-resize v:cursor-ns-resize',
  tap: 'slider-state-tap',
  drag: 'slider-state-drag',
}"/>
					</div>
				</div>
				<!-- Modal footer -->
				<div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
					<button @click="close" data-modal-hide="default-modal" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="js">
import {useModalStore} from "../../stores/ModalStore.js";
import {computed, onMounted, onUpdated, ref, watch} from "vue";
import {useCbcStore} from "../../stores/CbcStore.js";
import Slider from '@vueform/slider'

const props = defineProps({
	options: Array
})
const testValue = ref([0,10])
const store = useModalStore()
const cbcStore = useCbcStore()

const isOpen = computed(()=> store.getIsFilterModalOpen)
const headerContent = computed(()=> store.getHeaderContent)
const isCategorical = computed(()=> store.getFilterOptions.length < 10)
const filterOptions = computed(()=> store.getFilterOptions)
const allFilterOptions = computed(()=> store.getAllFilterOptions)
const filterKey = computed(()=> store.getFilterKey)

const selectedValue = ref(undefined)
const lastFilterKey = ref("")

const defaultRangeValues = ()=>{
	if(isCategorical.value) return [0,0]
	const numericFilterOptions = allFilterOptions.value.map(o => +o.value)
	return [Math.min(...numericFilterOptions), Math.max(...numericFilterOptions)]
}

const rangeValues = computed({
	get() {
		const filter = store.getFilters.find(filter => filter["filterKey"] === store.getFilterKey)
		if(filter === undefined) return defaultRangeValues()
		return [filter.minValue, filter.maxValue]
	},
	set(values) {
		let filter = store.getFilters.find(filter => filter["filterKey"] === store.getFilterKey)
		if(filter === undefined) {
			filter = {
				filterKey: store.getFilterKey,
				selectedValue: undefined,
				minValue: undefined,
				maxValue: undefined
			}
		}
		filter.minValue = values[0]
		filter.maxValue = values[1]
		store.addFilter(filter)
	}
})

function close(){
	store.setIsFilterModalOpen(false)
}

watch(selectedValue, (newSelectedValue) => {
	store.setFilters(store.getFilters.filter(filter => filter["filterKey"] !== store.getFilterKey))
	if(newSelectedValue !== undefined) {
		store.addFilter({
			filterKey: store.getFilterKey,
			selectedValue: newSelectedValue,
			minValue: undefined,
			maxValue: undefined
		})
	}
})

watch(filterKey, (newFilterKey) => {
	const filter = store.getFilters.find(filter => filter["filterKey"] !== newFilterKey.value)
	if(filter === undefined) return
	selectedValue.value = filter.selectedValue

})

</script>

<style scoped>

</style>

