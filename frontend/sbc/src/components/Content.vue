<template>
  <div class="custom-content-height overflow-y-auto w-full overflow-x-auto pb-2 pt-2" @scroll="updateViewPort">
    <div class="min-w-full grid leading-6 pt-2 gap-4 grid-container" :class="''"
         v-for="(cbc, idx) in filteredCbcs" :id="idx">
      <div v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
          <input
              class="p-2 rounded-md w-full w-32 text-right text-black" :value="cbc[cbcKey]"
              :type="type(cbcKey)"
              :placeholder="cbcKey"
              @input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
      </div>
			<div class="non-editable">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</div>
			<div class="flex justify-between col-span-3 gap-4">
			<div class="non-editable">{{cbc.confidence === undefined ? 'Unclassified' : cbc.confidence}}</div>
			<div class="non-editable">{{cbc.pred === undefined ? 'Unclassified' : cbc.pred }}</div>
			<Details :fun="()=>handleDetails(cbc)"/>
		</div>
    </div>
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {chartOptions} from "../lib/constants/ChartOptions.js";
import {computed, onUpdated, ref, onBeforeUpdate} from "vue";
import {editableCbcKeys} from "../lib/TableGrid.js"
import Details from "./icons/Details.vue";
import {useCbcStore} from "../stores/CbcStore.js";
import {router} from "../router/Router.js";

const options = chartOptions

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

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

function getLink(id){
	return `sbc_frontend/details/${id}`
}


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
	await router.push(`/sbc_frontend/details/${cbc.id}`)
}

onBeforeUpdate(()=>{
	console.log("Before Update")
	console.time("RenderTime")
})
onUpdated(()=>{
	console.timeEnd("RenderTime")
	console.log("Updated")
})
</script>

<style scoped>


.non-editable{
	@apply p-2 bg-gray-600 rounded-md w-full text-center select-none
}

.custom-content-height{
	max-height: calc(100% - 156px - 56px - 56px);
}
</style>
