<template>
	<div class="w-full overflow-x-auto " @scroll="updateViewPort" :style="`max-height: ${maxHeight}%`">
		<table class="table-auto min-w-[1300px] h-full relative">
			<TableHeader :is-detail-page="false"/>
			<tbody class="w-full overflow-x-auto pb-2 pt-2 block" >
			<tr class="grid leading-6 pt-2 gap-4 grid-container mb-2" :class="cbc.chartData ? ' ' : ''"
					v-for="(cbc, idx) in filteredCbcs" :id="idx">
				<td v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
					<input
						class="p-2 rounded-md w-full text-right text-black" :value="cbc[cbcKey]"
						:type="type(cbcKey)"
						:placeholder="cbcKey"
						@input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
				</td>
				<td class="non-editable w-full">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</td>
				<td class="non-editable w-full">{{cbc.confidence === undefined ? 'Unclassified' : getConfidenceString(cbc.confidence)}}</td>
				<td><Details :fun="()=>handleDetails(cbc)"/></td>
				<td class="grid-container " style="grid-column: span 12" v-if="cbc.chartData">
					<ChartSelection :cbc="cbc"/>
					<Chart  :cbc="cbc" :shap-type="cbc.shapType"/>
					<div class="col-span-2"></div>
					<div><List :fun="()=>handleShowClassifiers(cbc)"/></div>
				</td>
				<hr style="grid-column: span 12" v-if="newPatient(idx)"/>
			</tr>
			</tbody>
		</table>
	</div>

</template>

<script setup>
import {computed, ref, onBeforeMount, onUnmounted} from "vue";
import {editableCbcKeys} from "../../../lib/TableGrid.js"
import Details from "../../icons/Details.vue";
import {useCbcStore} from "../../../lib/stores/CbcStore.js";
import {router} from "../../../lib/router/Router.js";
import TableHeader from "./TableHeader.vue";
import Chart from "../../chart/Chart.vue";
import List from "../../icons/List.vue";
import ChartSelection from "../../chart/ChartSelection.vue";
import {updateScreenHeight} from "../../../lib/responsive/HeightRegularization.js";
import {submitCbcDetail} from "../../../lib/api/CBCDetails.js";

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

const screenHeight = ref(window.innerHeight)
const screenWidth = ref(window.innerWidth)
const maxHeight = ref(85)

updateScreenHeight(screenHeight, maxHeight)

function screenSizeHandler(){
	screenHeight.value = window.innerHeight
	screenWidth.value = window.innerWidth
	updateScreenHeight(screenHeight, maxHeight)
}

onBeforeMount(()=>{
	window.addEventListener("resize", screenSizeHandler)
})
onUnmounted(()=>{
	window.removeEventListener("resize", screenSizeHandler);
})
const store = useCbcStore()
const upperLimit = ref(50)
const lowerLimit = ref(0)

function valueInput(event, cbc, cbcKey){
	if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
	cbc[cbcKey] = +event.target.value
}

const filteredCbcs = computed(() =>{
	let preFilteredCbcs = [...store.getCbcMeasurements]
	const filteredCbcs =  preFilteredCbcs.filter((cbc, i) => i <= upperLimit.value && i>= lowerLimit.value)
	return filteredCbcs
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
	await submitCbcDetail(cbc)
}


async function handleShowClassifiers(cbc){
	await router.push(`/sbc_frontend/details/${cbc.id}`)
}

function newPatient(idx){
	if(idx >= filteredCbcs.value.length - 1) return false
	return filteredCbcs.value[idx].patientId !== filteredCbcs.value[idx + 1].patientId
}
function getConfidenceString(percent){
	const percentRounded = Math.round(percent*10)/10
	return `${percentRounded} %`
}
</script>

<style scoped>
</style>
