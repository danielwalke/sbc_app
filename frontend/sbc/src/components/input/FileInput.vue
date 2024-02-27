<template>
      <label for="file-input" class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600">
        File Upload
      </label>
      <input class="hidden" type="file" id="file-input" multiple @change="onFileInputChange" />
</template>

<script setup>
import {useCbcStore} from "../../stores/CbcStore.js";

const store = useCbcStore()
function onFileInputChange(e) {
	const file = e.target.files[0]
	store.readCbcFile(file)
}
</script>

<style scoped>

</style>
