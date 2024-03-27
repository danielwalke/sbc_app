<template>
			<button @click="fun">
				{{isLoading ? "Loading..." : "Submit"}}</button>
</template>

<script setup>
import {computed} from "vue";
import {useCbcStore} from "../../stores/CbcStore.js";

const props = defineProps({
	fun: Function
})
const store = useCbcStore()
const isLoading = computed(()=>store.isLoading)
</script>

<style scoped>

</style>
