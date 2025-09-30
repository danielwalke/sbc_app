<template>
	<div class="w-full overflow-x-auto overflow-y-hidden" :style="`height: ${maxHeight}%`">
		<div class="min-w-[1300px] w-full h-full text-xs md:text-sm lg:text-base mb-4">
      <TableHeader :is-detail-page="false"/>
			<div class="w-full overflow-x-auto p-[.25rem] lg:pt-2 block overflow-y-auto h-full pb-24" @scroll="updateViewPort">
        <div class="table-data grid leading-6 pt-2 grid-container mb-2" :class="cbc.chartData ? ' ' : ''"
            v-for="(cbc, idx) in filteredCbcs" :id="idx">
          <div v-for="cbcKey in editableCbcKeys" class="table-data flex justify-center items-center flex-col h-fit">
            <input
              class="p-[.33rem] lg:p-2 rounded-md w-full text-right text-black" :value="cbc[cbcKey]"
              :type="type(cbcKey)"
              :placeholder="cbcKey"
              @input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
          </div>
          <div class="table-data non-editable w-full">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</div>
          <div class="table-data non-editable w-full">{{cbc.confidence === undefined ? 'Unclassified' : getConfidenceString(cbc.confidence)}}</div>
          <div class="table-data"><Details :fun="()=>handleDetails(cbc)"/></div>
          <div class="table-data grid-container " style="grid-column: span 12" v-if="cbc.chartData">
            <ChartSelection :cbc="cbc"/>
            <Chart  :cbc="cbc" :shap-type="cbc.shapType"/>
            <div class="col-span-2">
              <button class="w-full" @click="()=> openLlmExplanationModal(cbc)">Ask Google Gemini</button>
            </div>
            <div><List :fun="()=>handleShowClassifiers(cbc)"/></div>
          </div>
          <hr style="grid-column: span 12" v-if="newPatient(idx)"/>
        </div>
			</div>
		</div>
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
import {useModalStore} from "../../../lib/stores/ModalStore.js";
import {receiveLlmExplanation} from "../../../lib/api/LlmExplanation.js";

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
const modalStore = useModalStore()
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
  const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
  const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

  return (
      rect.top < viewportHeight &&
      rect.left < viewportWidth &&
      rect.bottom > 0 &&
      rect.right > 0
  );
}

function updateViewPort(){
	// const lowerIdx = upperLimit.value- 2
  const lowerIdx = upperLimit.value- 20
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
	await router.push(`/sbc-shap/details/${cbc.id}`)
}

function newPatient(idx){
	if(idx >= filteredCbcs.value.length - 1) return false
	return filteredCbcs.value[idx].patientId !== filteredCbcs.value[idx + 1].patientId
}
function getConfidenceString(percent){
	const percentRounded = Math.round(percent*10)/10
	return `${percentRounded} %`
}

function openLlmExplanationModal(cbc){
  console.log(cbc)
  receiveLlmExplanation(cbc)

}
</script>

<style scoped>
</style>
