<script setup>

import SubmitButton from "./SubmitButton.vue";
import {submitCbcMeasurements} from "../../lib/api/CBCPredcitions.js";

function submit(){
  submitCbcMeasurements()
}
</script>

<template>
  <div class="">
    <div class="flex justify-center items-center gap-4 p-4">
      <SubmitButton :fun="submit"/>
    </div>
  </div>
</template>

<style scoped>

</style>