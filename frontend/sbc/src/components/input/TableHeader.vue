<template>
	<div class="grid-container">
		<div v-for="cbcKey in editableCbcKeys" class="grid-item">
			<div class="flex gap-3 pt-2">
				<p class="text-center">{{cbcKey}}</p>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction(cbcKey)" :classes="getFilterClass(cbcKey)"/>
				<Help :fun="() => helpCbcKeyFunction(cbcKey)"/>
			</div>
			<p class="text-center">({{unit(cbcKey)}})</p>
		</div>
		<div class="grid-item" >
			<div class="flex gap-2">
				Ground-truth
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('groundTruth')" :classes="getFilterClass('groundTruth')"/>
				<Help :fun="() => helpCbcKeyFunction('groundTruth')"/>
			</div>
		</div>
		<div class="grid-item" >
			<div class="flex gap-2">
				Confidence
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('confidence')" :classes="getFilterClass('confidence')"/>
				<Help :fun="() => helpCbcKeyFunction('confidence')"/>
			</div>
		</div>
		<div class="grid-item">
			<div class="flex gap-2">
				Prediction
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('pred')" :classes="getFilterClass('pred')"/>
				<Help :fun="() => helpCbcKeyFunction('pred')"/>
			</div>
		</div>
		<div class="grid-item" >
			<div class="flex gap-2" v-if="!isDetailPage">
				Details
				<Help :fun="() => helpCbcKeyFunction('details')"/>
			</div>
			<div class="flex gap-2" v-else>
				Classifier
				<Help :fun="() => helpCbcKeyFunction('classifier')"/>
			</div>
		</div>
	</div>
</template>

<script setup lang="js">
import {DEFAULT_CBC, UNITS_DICT} from "../../lib/constants/CBC_Constants.js";
import {computed} from "vue";
import {editableCbcKeys} from "../../lib/TableGrid.js"
import Help from "../icons/Help.vue";
import Filter from "../icons/Filter.vue";
import {useModalStore} from "../../stores/ModalStore.js";
import {useCbcStore} from "../../stores/CbcStore.js";
import {CBC_KEY_TO_DESCRIPTION} from "../../lib/constants/CBCDescriptions.js";

const modalStore = useModalStore()
const cbcStore = useCbcStore()

const props = defineProps({
	isDetailPage: Boolean
})

function unit(cbcKey){
	return UNITS_DICT[cbcKey]
}

function helpCbcKeyFunction(cbcKey){
	modalStore.setIsHelpModalOpen(true)
	modalStore.setHeaderContent(cbcKey)
	modalStore.setHelpMainContent(CBC_KEY_TO_DESCRIPTION[cbcKey])
}

function filterCbcKeyFunction(cbcKey){
	modalStore.setIsFilterModalOpen(true)
	modalStore.setHeaderContent(cbcKey)
	modalStore.setFilterKey(cbcKey)
}
const filterKeys = computed(()=>modalStore.getFilters.map(filter => filter["filterKey"]))

function getFilterClass(cbcKey){
	if(filterKeys.value.includes(cbcKey)) return "text-red-500"
	return ""
}
</script>

<style scoped>
.grid-item{
	@apply flex justify-center items-center flex-col h-fit
}

.grid-container {
	display: grid;
	grid-template-columns: repeat(13, minmax(0, 1fr));
	gap: 1rem;
}
</style>
