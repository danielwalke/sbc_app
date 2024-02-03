<template>

      <label for="file-input" class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600">
        File Upload
      </label>
      <input class="hidden" type="file" id="file-input" multiple @change="onInputChange" />

</template>

<script setup>
const props = defineProps({
    onInputChange:Function
})

</script>

<style scoped>

</style>