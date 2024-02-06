<template>
  <ResultColumn :title="title" class="mt-2">
    <div class="rounded-md bg-gray-600">{{value ? 'Sepsis' : 'Control'}}</div>
  </ResultColumn>
</template>

<script setup>
import ResultColumn from "./ResultColumn.vue";

defineProps({
  title: String,
  value: Boolean
})
</script>

<style scoped>

</style>
