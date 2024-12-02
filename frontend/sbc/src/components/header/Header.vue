<script setup>

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
  <div class="w-full text-xs md:text-sm lg:text-base">
    <div class="flex lg:justify-center items-center gap-2 md:gap-4 md:pb-4 flex-wrap md:pl-4 md:pr-4">
      <Home class="w-1/8"/>
      <GenericInput class="w-1/8"/>
      <button class="w-1/8 rounded-md shadow-md hover:scale-105 md:p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" @click="uploadTest">Test</button>
      <button class="w-1/8  rounded-md shadow-md hover:scale-105 md:p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" v-if="hasFilters" @click="resetFilters">Reset Filter</button>
      <PredictionSelection class="max-w-1/8"/>
      <div class="max-w-1/8 bg-gray-600 p-2 md:p-4 rounded-md">Samples count: {{cbc_counts}}</div>
    </div>

  </div>
</template>

<style scoped>

</style>