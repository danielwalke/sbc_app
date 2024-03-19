<template>
    <div class="flex justify-center w-full mt-4">
        <button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" @click="fun">
          {{isLoading ? "Loading..." : "Submit"}}</button>
    </div>
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
