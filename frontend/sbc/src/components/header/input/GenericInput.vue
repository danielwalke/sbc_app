<template>
	<button @click="open">
		Input
	</button>
</template>

<script setup lang="js">
import {useModalStore} from "../../../stores/ModalStore.js";

const modalStore = useModalStore()
function open(){
	modalStore.setIsInputModalOpen(true)
}
</script>

<style scoped>

</style>
