<template>
  <div class="flex justify-center items-center flex-col">
    <p>{{title}}</p>
    <div class="p-2 rounded-md bg-gray-600 mt-4" :style="slotStyle"><slot></slot></div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  slotStyle: {
    type: String,
    default() {
      return ""
    }
  }
})
</script>

<style scoped>

</style>