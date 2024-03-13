<template>
  <div class="w-full custom-height pt-4 pl-4 pb-4">
		<div class="flex justify-center items-center gap-4">
			<FileInput />
			<button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" v-if="hasFilters" @click="resetFilters">Reset Filter</button>
			<div class="bg-gray-600 p-4 rounded-md">Samples count: {{cbc_counts}}</div>
		</div>
		<TableHeader :is-detail-page="false"/>
		<Content/>
		<div class="p-2">
			<div class="flex justify-center w-full mt-4">
				<button
				@click="addCbcMeasurement"
				class="flex justify-center items-center rounded-full border-2 text-white h-fit w-fit p-4 text-2xl pt-2 pb-2">+
				</button>
			</div>
			<SubmitButton :fun="submit"/>
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
import {useModalStore} from "../stores/ModalStore.js";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useCbcStore()

const has_predictions = computed(()=>store.has_predictions)
const cbc_counts  = computed(()=>store.getCbcMeasurements.length)

function addCbcMeasurement(){
	store.addCbcMeasurements({...DEFAULT_CBC})
}

const modalStore = useModalStore()

const hasFilters = computed(()=> modalStore.getFilters.length > 0)

function resetFilters(){
	modalStore.setFilters([])
}

function submit(){
	store.submitCbcMeasurements()
}
</script>

<style scoped>
</style>
