<template>
	<div class="w-full overflow-x-auto " @scroll="updateViewPort" :style="`max-height: ${maxHeight}%`">
		<table class="table-auto min-w-[1300px] h-full relative">
			<TableHeader :is-detail-page="false"/>
			<tbody class="w-full overflow-x-auto pb-2 pt-2 block" >
			<tr class="grid leading-6 pt-2 gap-4 grid-container mb-2" :class="cbc.chartData ? ' ' : ''"
					v-for="(cbc, idx) in filteredCbcs" :id="idx">
				<td v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
					<input
						class="p-2 rounded-md w-full w-32 text-right text-black" :value="cbc[cbcKey]"
						:type="type(cbcKey)"
						:placeholder="cbcKey"
						@input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
				</td>
				<td class="non-editable w-full">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</td>
				<td class="non-editable w-full">{{cbc.confidence === undefined ? 'Unclassified' : cbc.confidence}}</td>
				<td class="non-editable w-full">{{cbc.pred === undefined ? 'Unclassified' : cbc.pred }}</td>
				<td><Details :fun="()=>handleDetails(cbc)"/></td>
				<td class="grid-container " style="grid-column: span 13" v-if="cbc.chartData">
					<div class="col-span-2"></div>
					<Chart  :cbc="cbc"/>
					<div class="col-span-3"></div>
					<div><List :fun="()=>handleShowClassifiers(cbc)"/></div>
				</td>
			</tr>
			</tbody>
		</table>
	</div>

</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {chartOptions} from "../../lib/constants/ChartOptions.js";
import {computed, onUpdated, ref, onBeforeUpdate, onBeforeMount, onUnmounted, watch} from "vue";
import {editableCbcKeys} from "../../lib/TableGrid.js"
import Details from "./../icons/Details.vue";
import {useCbcStore} from "../../stores/CbcStore.js";
import {router} from "../../router/Router.js";
import TableHeader from "./TableHeader.vue";
import Chart from "../chart/Chart.vue";
import List from "../icons/List.vue";

const options = chartOptions

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

const screenHeight = ref(window.innerHeight)
const screenWidth = ref(window.innerWidth)
const maxHeight = ref(80)
updateScreenHeight()
function updateScreenHeight(){
	if(screenHeight.value <= 700){
		return maxHeight.value = 55
	}
	if(screenHeight.value <= 850){
		return maxHeight.value = 65
	}
	if(screenHeight.value <= 1000){
		return maxHeight.value = 70
	}
	if(screenHeight.value <= 1200){
		return maxHeight.value = 75
	}
	if(screenHeight.value <= 1300){
		return maxHeight.value = 80
	}
}

function screenSizeHandler(){
	screenHeight.value = window.innerHeight
	screenWidth.value = window.innerWidth
	updateScreenHeight()
}

onBeforeMount(()=>{
	window.addEventListener("resize", screenSizeHandler)
})
onUnmounted(()=>{
	window.removeEventListener("resize", screenSizeHandler);
})
const store = useCbcStore()
const has_predictions = computed(()=>store.has_predictions)
const upperLimit = ref(50)
const lowerLimit = ref(0)

function valueInput(event, cbc, cbcKey){
	if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
	cbc[cbcKey] = +event.target.value
}

const filteredCbcs = computed(() =>{
	let preFilteredCbcs = [...store.getCbcMeasurements]
	return preFilteredCbcs.filter((cbc, i) => i <= upperLimit.value && i>= lowerLimit.value)
})


function isInViewport(element) {
	const rect = element.getBoundingClientRect();
	return (
		rect.top >= 0 &&
		rect.left >= 0 &&
		rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
		rect.right <= (window.innerWidth || document.documentElement.clientWidth)
	);
}

function updateViewPort(){
	const lowerIdx = upperLimit.value-2
	const lowerElement = document.getElementById(lowerIdx)
	if(lowerElement && isInViewport(lowerElement)){
		upperLimit.value +=50
	}
}

async function handleDetails(cbc){
	store.setHasPredictions(true)
	store.submitCbcDetail(cbc)
}


async function handleShowClassifiers(cbc){
	await router.push(`/sbc_frontend/details/${cbc.id}`)
}

</script>

<style scoped>

.custom-content-height{
	max-height: calc(100% - 156px - 56px - 144px);
}
</style>
