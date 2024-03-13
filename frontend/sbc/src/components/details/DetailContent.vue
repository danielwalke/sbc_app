<template>
	<div class="custom-height overflow-y-auto w-full">
		<TableHeader :is-detail-page="true" class="pt-4"/>
		<div class="w-full grid leading-6 pt-2 gap-4 grid-container pl-4 pr-4" :class="''"
				 v-for="(cbc, idx) in cbcOverClassifiers" :id="idx">
			<div v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
				<input
					class="p-2 rounded-md w-full w-32 text-right text-black" :value="cbc[cbcKey]"
					:type="type(cbcKey)"
					:placeholder="cbcKey"
					@input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
			</div>
			<div class="non-editable">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</div>
			<div class="flex justify-between col-span-3 gap-4" >
				<div class="non-editable">{{cbc.confidence === undefined ? 'Unclassified' : cbc.confidence}}</div>
				<div class="non-editable">{{cbc.pred === undefined ? 'Unclassified' : cbc.pred }}</div>
				<div class="non-editable">{{cbc.classifier}}</div>
			</div>

			<div class="col-span-2" v-if="hasPredictionDetails"></div>
			<div class="col-span-7 flex justify-center max-h-48" v-if="hasPredictionDetails">
				<Bar :data="cbc.chartData" :options="chartOptions"/>
			</div>
		</div>
		<SubmitButton :fun="submitDetails"/>
	</div>
</template>

<script setup lang="js">
import {editableCbcKeys} from "../../lib/TableGrid.js"
import {useCbcStore} from "../../stores/CbcStore.js";
import {computed} from "vue";
import {useRoute, useRouter} from "vue-router";
import TableHeader from "../input/TableHeader.vue";
import SubmitButton from "../results/SubmitButton.vue";
import { Bar } from 'vue-chartjs'
import {chartOptions} from "../../lib/constants/ChartOptions.js";
const router = useRouter()
const route = useRoute()

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}
function valueInput(event, cbc, cbcKey){
	if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
	cbc[cbcKey] = +event.target.value
}

const cbcStore = useCbcStore()
cbcStore.setHasPredictionDetails(false)
const hasPredictionDetails = computed(()=> cbcStore.getHasPredictionDetails)
const cbcOverClassifiers = computed(()=> cbcStore.getCbcOverClassifiers)

function submitDetails(){
	cbcStore.submitCbcMeasurementDetails()
}
</script>

<style scoped>

.non-editable{
	@apply p-2 bg-gray-600 rounded-md w-full text-center select-none
}

</style>
