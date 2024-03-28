<template>
  <div class="w-full custom-height pt-4 pl-4 pb-4">
		<div class="flex justify-center items-center gap-4 pb-4">
			<FileInput />
			<button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" v-if="hasFilters" @click="resetFilters">Reset Filter</button>
			<div class="bg-gray-600 p-4 rounded-md">Samples count: {{cbc_counts}}</div>
			<ClassifierSelector/>
		</div>
		<Content/>
		<div class="p-2">
			<div class="flex justify-center w-full mt-4">
				<button
				@click="addCbcMeasurement"
				class="flex justify-center items-center rounded-full border-2 text-white h-fit w-fit p-4 text-2xl pt-2 pb-2">+
				</button>
			</div>
			<div class="flex justify-center items-center gap-4 p-4">
				<SubmitButton :fun="submit"/>
				<button v-if="has_predictions" @click="download">Download</button>
				<div class="non-editable" style="padding: 1rem;" v-if="has_predictions">AUROC: {{auroc}}</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import {computed, ref} from "vue";
import SubmitButton from "./results/SubmitButton.vue";
import FileInput from "./input/FileInput.vue";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import Content from "./input/Content.vue";
import TableHeader from "./input/TableHeader.vue";
import {DEFAULT_CBC} from "../lib/constants/CBC_Constants.js";
import {useCbcStore} from "../stores/CbcStore.js";
import {useModalStore} from "../stores/ModalStore.js";
import { v4 as uuid } from 'uuid';
import ClassifierSelector from "./input/ClassifierSelector.vue";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useCbcStore()

const has_predictions = computed(()=>store.has_predictions)
const cbc_counts  = computed(()=>store.getCbcMeasurements.length)
const auroc = computed(()=> store.getAuroc)

function addCbcMeasurement(){
	store.addCbcMeasurements({...DEFAULT_CBC, uuid: uuid()})
}

const modalStore = useModalStore()

const hasFilters = computed(()=> modalStore.getFilters.length > 0)

function resetFilters(){
	modalStore.setFilters([])
}

function submit(){
	store.submitCbcMeasurements()
}

function download(){
	store.download()
}

</script>

<style scoped>
</style>
