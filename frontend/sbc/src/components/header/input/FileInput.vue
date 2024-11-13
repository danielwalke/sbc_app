<template>
	<label for="file-input" class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600">
		New file
	</label>
	<input class="hidden" type="file" id="file-input" multiple @change="onFileInputChange" />
</template>

<script setup>
import {useCbcStore} from "../../../lib/stores/CbcStore.js";
import {useModalStore} from "../../../lib/stores/ModalStore.js";
import {readCbcFile} from "../../../lib/input/FileReader.js";

const store = useCbcStore()
const modalStore = useModalStore()
function onFileInputChange(e) {
	const file = e.target.files[0]
	readCbcFile(file)
	modalStore.setIsInputModalOpen(false)
}
</script>

<style scoped>

</style>
