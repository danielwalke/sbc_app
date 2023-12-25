<template>
  <ResultColumn :title="title">
    {{Math.round(value*10000)/10000}}
  </ResultColumn>
</template>

<script setup>
import ResultColumn from "./ResultColumn.vue";

defineProps({
  title: String,
  value: Number
})
</script>

<style scoped>

</style>