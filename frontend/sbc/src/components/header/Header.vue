<script setup>

import {predictionTypes} from "../../lib/constants/PredcitionTypes.js";
import Home from "./navigation/Home.vue";
import GenericInput from "./input/GenericInput.vue";
import PredictionSelection from "./predictionSelection/PredictionSelection.vue";
import {computed} from "vue";
import {useModalStore} from "../../lib/stores/ModalStore.js";
import {getTestFile} from "../../lib/testCsvs/leipzig_test_100000.js";
import {useCbcStore} from "../../lib/stores/CbcStore.js";
import {parseFile} from "../../lib/input/FileParser.js";
import {submitCbcMeasurements} from "../../lib/api/CBCPredcitions.js";

const store = useCbcStore()
const modalStore = useModalStore()
const cbc_counts  = computed(()=>store.getCbcMeasurements.length)
const hasFilters = computed(()=> modalStore.getFilters.length > 0)

function resetFilters(){
  modalStore.setFilters([])
}

async function uploadTest() {
  store.setIsLoading(true)
  store.setCbcMeasurements([])
  const testFile = getTestFile()
  parseFile(testFile)
  store.setIsLoading(false)
  await submitCbcMeasurements()
}

</script>

<template>
  <div class=" w-full overflow-x-scroll sm:overflow-x-hidden">
    <div class="flex justify-center items-center gap-4 pb-4 min-w-max flex-wrap pl-4 pr-4">
      <Home/>
      <GenericInput/>
      <button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" @click="uploadTest">Test</button>
      <button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" v-if="hasFilters" @click="resetFilters">Reset Filter</button>
      <PredictionSelection :options="predictionTypes"/>
      <div class="bg-gray-600 p-4 rounded-md">Samples count: {{cbc_counts}}</div>
    </div>

  </div>
</template>

<style scoped>

</style>