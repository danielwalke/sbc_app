<template>
  <div class="max-h-[80%] overflow-y-auto w-full" @scroll="updateViewPort">
    <div class="w-full grid leading-6 pt-2 gap-4 grid-container" :class="''"
         v-for="(cbc, idx) in filteredCbcs" :id="idx">
      <div v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
          <input
              class="p-2 rounded-md w-full w-32 text-right text-black" :value="cbc[cbcKey]"
              :type="type(cbcKey)"
              :placeholder="cbcKey"
              @input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
      </div>
			<div class="non-editable">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth ? 'Sepsis': 'Control'}}</div>
			<div class="flex justify-between col-span-3 gap-4" v-if="has_predictions">
			<div class="non-editable">{{cbc.pred_proba === undefined ? 'Unclassified' : Math.round((1-Math.abs(cbc.pred_proba*PREDICTION_THRESHOLD)/PREDICTION_THRESHOLD)*10000)/100}}</div>
			<div class="non-editable">{{cbc.pred === undefined ? 'Unclassified' : cbc.pred ? 'Sepsis' : 'Control' }}</div>
			<Details/>
		</div>
		<div v-else class="col-span-4"></div>

      <div class="col-span-2" v-if="has_predictions"></div>
      <div class="col-span-7 flex justify-center max-h-48" v-if="has_predictions && cbc.chartData">
        <Bar :data="cbc.chartData" :options="options"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {chartOptions} from "../lib/constants/ChartOptions.js";
import {computed, ref} from "vue";
import {FALSE_NEGATIVE, FALSE_POSITIVE, TRUE_NEGATIVE, TRUE_POSITIVE} from "../lib/constants/FilterOptions.js";
import {editableCbcKeys} from "../lib/TableGrid.js"
import {PREDICTION_THRESHOLD} from "../lib/constants/CBC_Constants.js";
import Details from "./icons/Details.vue";
import {useCbcStore} from "../stores/CbcStore.js";

const options = chartOptions

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

const store = useCbcStore()
const has_predictions = computed(()=>store.has_predictions)
const selectedFilterValue = computed(()=>store.getSelectedFilterValue)
const upperLimit = ref(50)
const lowerLimit = ref(0)

function valueInput(event, cbc, cbcKey){
	if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
	cbc[cbcKey] = +event.target.value
}

const filteredCbcs = computed(() =>{
  let preFilteredCbcs = [...store.getCbcMeasurements]
  if(!selectedFilterValue.value) return preFilteredCbcs.filter((cbc, i) => i <= upperLimit.value && i>= lowerLimit.value)

  if(selectedFilterValue.value === TRUE_POSITIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc, i) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.pred === true && cbc.groundTruth === true)
    })
  }
  if(selectedFilterValue.value === TRUE_NEGATIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc, i) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.groundTruth === false && cbc.pred === false)
    })
  }

  if(selectedFilterValue.value === FALSE_POSITIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.groundTruth === false && cbc.pred === true)
    })
  }

  if(selectedFilterValue.value === FALSE_NEGATIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.groundTruth === true && cbc.pred === false)
    })
  }
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

</script>

<style scoped>
.grid-container {
	display: grid;
	grid-template-columns: repeat(13, minmax(0, 1fr));
	gap: 1rem;
}

.non-editable{
	@apply p-2 bg-gray-600 rounded-md w-full text-center select-none
}
</style>
