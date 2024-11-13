<template>
	<div class="w-full custom-height select-none">
		<Back/>
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
					<td class="non-editable">{{cbc.confidence === undefined ? 'Unclassified' : getConfidenceString(cbc.confidence)}}</td>
					<td class="non-editable">{{cbc.classifier}}</td>
          <ChartSelection :cbc="cbc"/>
          <Chart  :cbc="cbc" :shap-type="cbc.shapType"/>
				</tr>
				</tbody>
			</table>
		</div>
		<div class="flex justify-center pt-4"><SubmitButton :fun="submitDetails" class="pb-2"/></div>
	</div>
</template>

<script setup lang="js">
import {editableCbcKeys} from "../../lib/TableGrid.js"
import {useCbcStore} from "../../lib/stores/CbcStore.js";
import {computed, onMounted, watch} from "vue";
import TableHeader from "../header/input/TableHeader.vue";
import SubmitButton from "../submit/SubmitButton.vue";
import Chart from "../chart/Chart.vue";
import Back from "../header/navigation/Back.vue";
import ChartSelection from "../chart/ChartSelection.vue";
import {submitCbcClassifierDetails} from "../../lib/api/CBCClassifierDetails.js";
import {initializeClassifiersCbcs} from "../../lib/classifierDetails/InitializeClassifierObjects.js";

const cbcStore = useCbcStore()
initializeClassifiersCbcs()
cbcStore.setHasPredictionDetails(false)

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}

const cbcOverClassifiers = computed(()=> cbcStore.getCbcOverClassifiers) // ref(cbcStore.getCbcOverClassifiers)

const cbcOverClassifiersComputed =computed(()=> cbcStore.getCbcOverClassifiers)

watch(cbcOverClassifiersComputed, function(newValue){
	cbcOverClassifiers.value = newValue
})

function valueInput(event, edited_cbc, cbcKey){
	for(const cbc of cbcOverClassifiers.value){
		if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
		cbc[cbcKey] = +event.target.value
	}
	cbcStore.setCbcOverClassifiers(cbcOverClassifiers.value)
}

onMounted(()=>{
	if(cbcStore.getCbcOverClassifiers.some(item => item.age === undefined)){
		return
	}
	submitDetails()
})

function submitDetails(){
  submitCbcClassifierDetails()
}

function getConfidenceString(percent){
	const percentRounded = Math.round(percent*10)/10
	return `${percentRounded} %`
}
</script>

<style scoped>

.non-editable{
	@apply p-2 bg-gray-600 rounded-md w-full text-center select-none
}

</style>
