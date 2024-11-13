<template>
  <div class="custom-content-height overflow-y-auto w-full overflow-x-auto pb-2 pt-2" @scroll="updateViewPort">
    <div class="min-w-full grid leading-6 pt-2 gap-4 grid-container" :class="''"
         v-for="(cbc, idx) in filteredCbcs" :id="idx">
      <div v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
          <input
              class="p-2 rounded-md w-full text-right text-black" :value="cbc[cbcKey]"
              :type="type(cbcKey)"
              :placeholder="cbcKey"
              @input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
      </div>
			<div class="non-editable">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</div>
			<div class="flex justify-between col-span-2 gap-4">
			<div class="non-editable">{{cbc.confidence === undefined ? 'Unclassified' : cbc.confidence}}</div>
			<div class="non-editable">{{cbc.pred === undefined ? 'Unclassified' : cbc.pred }}</div>
			<Details :fun="()=>handleDetails(cbc)"/>
		</div>
    </div>
  </div>
</template>

<script setup>
import {computed, onUpdated, ref, onBeforeUpdate} from "vue";
import {editableCbcKeys} from "../lib/TableGrid.js"
import Details from "./icons/Details.vue";
import {useCbcStore} from "../lib/stores/CbcStore.js";
import {router} from "../lib/router/Router.js";

const store = useCbcStore()
const upperLimit = ref(50)
const lowerLimit = ref(0)

const filteredCbcs = computed(() =>{
  let preFilteredCbcs = [...store.getCbcMeasurements]
  return preFilteredCbcs.filter((cbc, i) => i <= upperLimit.value && i>= lowerLimit.value)
})

onBeforeUpdate(()=>{
  console.log("Before Update")
  console.time("RenderTime")
})

onUpdated(()=>{
  console.timeEnd("RenderTime")
  console.log("Updated")
})

function valueInput(event, cbc, cbcKey){
	if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
	cbc[cbcKey] = +event.target.value
}

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

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


</script>

<style scoped>


.non-editable{
	@apply p-2 bg-gray-600 rounded-md w-full text-center select-none
}

.custom-content-height{
	max-height: calc(100% - 156px - 56px - 56px);
}
</style>
