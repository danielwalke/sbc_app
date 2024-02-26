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
		<div class="flex justify-between col-span-4 gap-4" v-if="has_predictions">
			<div class="non-editable">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth ? 'Sepsis': 'Control'}}</div>
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
import ResultColumnProba from "./results/ResultColumnProba.vue";
import ResultColumnPred from "./results/ResultColumnPred.vue";
import {chartOptions} from "../lib/constants/ChartOptions.js";
import {computed, ref} from "vue";
import {FALSE_NEGATIVE, FALSE_POSITIVE, TRUE_NEGATIVE, TRUE_POSITIVE} from "../lib/constants/FilterOptions.js";
import {editableCbcKeys} from "../lib/TableGrid.js"
import {PREDICTION_THRESHOLD} from "../lib/constants/CBC_Constants.js";
import Details from "./icons/Details.vue";

const options = chartOptions

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

const props = defineProps({
  cbcs:Array,
  shaps:Array,
  valueInput:Function,
  selectedFilterValue: String|undefined,
  has_predictions: Boolean
})

const upperLimit = ref(50)
const lowerLimit = ref(0)
const filteredCbcs = computed(() =>{
  let preFilteredCbcs = [...props.cbcs]
  if(!props.selectedFilterValue) return preFilteredCbcs.filter((cbc, i) => i <= upperLimit.value && i>= lowerLimit.value)

  if(props.selectedFilterValue === TRUE_POSITIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc, i) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.pred === true && cbc.groundTruth === true)
    })
  }
  if(props.selectedFilterValue === TRUE_NEGATIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc, i) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.groundTruth === false && cbc.pred === false)
    })
  }

  if(props.selectedFilterValue === FALSE_POSITIVE){
    preFilteredCbcs = preFilteredCbcs.filter((cbc) => {
      if(cbc.pred === undefined || cbc.groundTruth === undefined) return true
      return (cbc.groundTruth === false && cbc.pred === true)
    })
  }

  if(props.selectedFilterValue === FALSE_NEGATIVE){
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
