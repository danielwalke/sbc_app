<template>
	<div class="w-full custom-height pt-4 pl-4 pb-4">
		<div class="flex justify-center items-center gap-4 pb-4">
			<FileInput />
			<button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" @click="uploadTest">Test</button>
			<button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" v-if="hasFilters" @click="resetFilters">Reset Filter</button>
			<div class="bg-gray-600 p-4 rounded-md">Samples count: {{cbc_counts}}</div>
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
import {getTestFile} from "../../testCsvs/leipzig_test_100000.js";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useCbcStore()

const has_predictions = computed(()=>store.has_predictions)
const cbc_counts  = computed(()=>store.getCbcMeasurements.length)

function addCbcMeasurement(){
	store.unshiftCbcMeasurements({...DEFAULT_CBC})
}

const modalStore = useModalStore()

const hasFilters = computed(()=> modalStore.getFilters.length > 0)

function resetFilters(){
	store.setCbcMeasurements(store.getCbcCopy)
	modalStore.setFilters([])
}

function submit(){
	store.submitCbcMeasurements()
}

async function uploadTest() {
	store.setIsLoading(true)
	store.setCbcMeasurements([])
	const testFile = getTestFile()
	store.parseFile(testFile)
	store.setIsLoading(false)

}
</script>

<style scoped>
</style>
