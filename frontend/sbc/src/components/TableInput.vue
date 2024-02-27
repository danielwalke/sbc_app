<template>
  <div class="w-full h-full pt-4 pl-4 pb-4">
		<div class="flex justify-center items-center gap-4">
			<FileInput />
			<FilterDropdown v-if="has_predictions && cbcs[0].groundTruth !== undefined"/>
		</div>
		<TableHeader/>
		<Content/>
		<div>
			<div class="flex justify-center w-full mt-4"><button
				@click="addCbcMeasurement"
				class="flex justify-center items-center rounded-full border-2 text-white h-fit w-fit p-4 text-2xl pt-2 pb-2">+</button></div>
			<SubmitButton/>
		</div>
	</div>
</template>

<script setup>
import {computed, ref} from "vue";
import SubmitButton from "./results/SubmitButton.vue";
import FileInput from "./input/FileInput.vue";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import Content from "./Content.vue";
import FilterDropdown from "./FilterDropdown.vue";
import TableHeader from "./input/TableHeader.vue";
import {DEFAULT_CBC} from "../lib/constants/CBC_Constants.js";
import {useCbcStore} from "../stores/CbcStore.js";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useCbcStore()

const has_predictions = computed(()=>store.has_predictions)
const cbcs  = computed(()=>store.getCbcMeasurements)

function addCbcMeasurement(){
	store.addCbcMeasurements({...DEFAULT_CBC})
}

</script>

<style scoped>

</style>
