<script setup>
import {useCbcStore} from "../../lib/stores/CbcStore.js";

const props = defineProps({
  cbc: Object
})

const cbcStore = useCbcStore()

function hasTimeSeriesInformation(selected_cbc){
  const cbcIds = cbcStore.getUnfilteredCbcMeasurements.map(cbc => cbc.patientId)
  const cbcIdCounter = {}
  for(const cbcId of cbcIds){
    if (!(cbcId in cbcIdCounter)){
      cbcIdCounter[cbcId] = 0
    }
    cbcIdCounter[cbcId] += 1
  }
  return cbcIdCounter[selected_cbc.patientId] > 1
}
</script>

<template>
  <div class="col-span-2 flex flex-col gap-2 pt-0 pb-2 pl-2 pr-2">
    <button v-if="hasTimeSeriesInformation(cbc)" class="h-14" @click="()=> props.cbc.shapType = 'combined'" :class="props.cbc.shapType === 'combined' ? '' : 'bg-gray-700 hover:bg-gray-600' ">combined</button>
    <button v-if="hasTimeSeriesInformation(cbc)" class="h-14" @click="()=> props.cbc.shapType = 'original'" :class="props.cbc.shapType === 'original' ? '' : 'bg-gray-700 hover:bg-gray-600' ">Sample</button>
    <button v-if="hasTimeSeriesInformation(cbc)" class="h-14" @click="()=> props.cbc.shapType = 'time'" :class="props.cbc.shapType === 'time' ? '' : 'bg-gray-700 hover:bg-gray-600' ">Time</button>
  </div>
</template>

<style scoped>

</style>