<template>
  <div class="flex justify-center items-center flex-col">
    <p>{{title}}</p>
    <div class="p-2 rounded-md bg-gray-600 mt-4"><slot></slot></div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String
})
</script>

<style scoped>

</style>