<template>
  <ResultColumn :title="title" :slotStyle="getColor(value)">
    {{Math.round(value*10000)/10000}}
  </ResultColumn>
</template>

<script setup>
import ResultColumn from "./ResultColumn.vue";

defineProps({
  title: String,
  value: Number
})

function getColor(value){
  return `background-color: rgb(${255/.6241*value-164.55}, 0, ${255-255/.3759*value})`
}
</script>

<style scoped>

</style>
