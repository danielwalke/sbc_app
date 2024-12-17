<script setup>
import {useModalStore} from "../../../lib/stores/ModalStore.js";
import Slider from '@vueform/slider'

const modalStore = useModalStore()
function customizeThreshold(){
  modalStore.setIsSensitivityModelOpen(true)
}

</script>

<template>
  <button @click="customizeThreshold">Sensitivity</button>
</template>

<style scoped>

</style>