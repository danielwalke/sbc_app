<template>
  <div class="max-h-[80%] overflow-y-auto" @scroll="updateViewPort">
    <div class="w-full grid leading-6 pt-2 gap-4 pl-4 pr-4" :class="'grid-cols-10'"
         v-for="(cbc, idx) in filteredCbcs" :id="idx">
      <div v-for="cbcKey in cbcKeys" class="flex justify-center items-center flex-col h-fit">
          <p class="text-center">{{cbcKey}}</p>
          <p class="text-center">({{unit(cbcKey)}})</p>
          <input
              class="p-2 rounded-md w-full w-32 text-right text-black" :value="cbc[cbcKey]"
              :type="type(cbcKey)"
              :placeholder="cbcKey"
              @input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
      </div>
		<div class="flex justify-between col-span-2" v-if="has_predictions">
		  <ResultColumnPred title="Ground-truth" v-if="cbc.groundTruth !== undefined"
							:value="cbc.groundTruth"/>
		  <ResultColumnProba v-if="cbc.pred_proba !== undefined" title="Sepsis-prob." :value="cbc.pred_proba" />
		  <ResultColumnPred v-if="cbc.pred !== undefined" title="Prediction" :value="cbc.pred"/>
		</div>
		<div v-else class="col-span-2"></div>

      <div class="col-span-1" v-if="has_predictions"></div>
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
import {DEFAULT_CBC, UNITS_DICT} from "../lib/constants/CBC_Constants.js";
import {chartOptions} from "../lib/constants/ChartOptions.js";
import {computed, ref} from "vue";
import {FALSE_NEGATIVE, FALSE_POSITIVE, TRUE_NEGATIVE, TRUE_POSITIVE} from "../lib/constants/FilterOptions.js";

const options = chartOptions

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

const props = defineProps({
  cbcs:Array,
  shaps:Array,
  valueInput:Function,
  selectedFilterValue: String|undefined,
  has_predictions: Boolean
})

const upperLimit = ref(10)
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
	console.log(preFilteredCbcs)
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
const cbcKeys = computed(() => {
  return Object.keys(DEFAULT_CBC).filter(key => !["groundTruth", "pred", "pred_proba"].includes(key))
})


function unit(cbcKey){
  return UNITS_DICT[cbcKey]
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
    upperLimit.value +=10
  }
}

</script>

<style scoped>

</style>
