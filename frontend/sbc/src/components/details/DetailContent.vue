<template>
	<div class="w-full custom-height">
		<div class="w-full overflow-x-auto max-h-[80%]">
			<table class="table-auto min-w-[1300px] h-full relative">
				<TableHeader :is-detail-page="true" class="pt-4"/>
				<tbody>
				<tr class="w-full grid leading-6 pt-2 gap-4 grid-container pl-4 pr-4" :class="''"
						v-for="(cbc, idx) in cbcOverClassifiers" :id="idx">
					<td v-for="cbcKey in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
						<input
							class="p-2 rounded-md w-full w-32 text-right text-black" :value="cbc[cbcKey]"
							:type="type(cbcKey)"
							:placeholder="cbcKey"
							@input="event => valueInput(event, cbc, cbcKey)" @change="event => valueInput(event, cbc, cbcKey)"/>
					</td>
					<td class="non-editable">{{cbc.groundTruth === undefined ? 'Unknown' : cbc.groundTruth}}</td>

					<td class="non-editable">{{cbc.confidence === undefined ? 'Unclassified' : cbc.confidence}}</td>
					<td class="non-editable">{{cbc.pred === undefined ? 'Unclassified' : cbc.pred }}</td>
					<td class="non-editable">{{cbc.classifier}}</td>

					<td class="col-span-2" v-if="hasPredictionDetails"></td>
					<td class="col-span-7 flex justify-center max-h-48" v-if="hasPredictionDetails">
						<Bar :data="cbc.chartData" :options="chartOptions"/>
					</td>
				</tr>
				</tbody>
			</table>
		</div>
		<div class="flex justify-center pt-4"><SubmitButton :fun="submitDetails" class="pb-2"/></div>
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
