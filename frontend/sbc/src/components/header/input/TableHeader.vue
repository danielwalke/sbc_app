<template>
	<div class="w-full text-xs md:text-sm lg:text-base" style="background-color: #242424">
	<div class="grid-container">
		<div v-for="cbcKey in editableCbcKeys" class="grid-item">
			<div class="header-item pt-2">
				<div class="flex gap-2 text-center hover:cursor-pointer" @click="()=> sortData(cbcKey)">{{getCbcLabel(cbcKey)}}
					<ChevoronUp v-if="isSorted(cbcKey) && isAscending(cbcKey)"/>
					<ChevronDown v-if="isSorted(cbcKey) && !isAscending(cbcKey)"/>
				</div>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction(cbcKey)" :classes="getFilterClass(cbcKey)"/>
				<Help :fun="() => helpCbcKeyFunction(cbcKey)"/>
			</div>
			<p class="text-center">({{unit(cbcKey)}})</p>
		</div>
		<div class="grid-item" >
			<div class="header-item">
				<div class="flex gap-2 text-center hover:cursor-pointer" @click="()=> sortData('groundTruth')">Ground-truth
					<ChevoronUp v-if="isSorted('groundTruth') && isAscending('groundTruth')"/>
					<ChevronDown v-if="isSorted('groundTruth') && !isAscending('groundTruth')"/>
				</div>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('groundTruth')" :classes="getFilterClass('groundTruth')"/>
				<Help :fun="() => helpCbcKeyFunction('groundTruth')"/>
			</div>
		</div>
		<div class="grid-item" >
			<div class="header-item">
				<div class="flex gap-2 text-center hover:cursor-pointer" @click="()=> sortData('confidence')">Sepsis risk
					<ChevoronUp v-if="isSorted('confidence') && isAscending('confidence')"/>
					<ChevronDown v-if="isSorted('confidence') && !isAscending('confidence')"/>
				</div>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('confidence')" :classes="getFilterClass('confidence')"/>
				<Help :fun="() => helpCbcKeyFunction('confidence')"/>
			</div>
		</div>
		<div class="header-item" >
			<div class="flex gap-2" v-if="!isDetailPage">
				Details
				<Help :fun="() => helpCbcKeyFunction('details')"/>
			</div>
			<div class="header-item" v-else>
				Classifier
				<Help :fun="() => helpCbcKeyFunction('classifier')"/>
			</div>
		</div>
	</div>
	</div>
</template>

<script setup lang="js">
import {UNITS_DICT} from "../../../lib/constants/CBC_Constants.js";
import {computed} from "vue";
import {editableCbcKeys} from "../../../lib/TableGrid.js"
import Help from "../../icons/Help.vue";
import Filter from "../../icons/Filter.vue";
import {useModalStore} from "../../../lib/stores/ModalStore.js";
import {useCbcStore} from "../../../lib/stores/CbcStore.js";
import {CBC_KEY_TO_DESCRIPTION} from "../../../lib/constants/CBCDescriptions.js";
import ChevoronUp from "../../icons/ChevoronUp.vue";
import ChevronDown from "../../icons/ChevronDown.vue";

const modalStore = useModalStore()
const cbcStore = useCbcStore()

const props = defineProps({
	isDetailPage: Boolean
})


const sortKeys = computed(()=> cbcStore.getSortKeys)

function isSorted(attributeName){
  return sortKeys.value.map(sortKey => sortKey.attributeName).includes(attributeName)
}

function isAscending(attributeName){
  return sortKeys.value.find(sortKey => sortKey.attributeName === attributeName)?.ascending
}

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

function sortData(cbcKey){
	cbcStore.sortData(cbcKey)
}

function getCbcLabel(cbcKey){
  if(cbcKey === "order") return "time"
  if(cbcKey === "patientId") return "Id"
  return cbcKey
}
</script>

<style scoped>
.grid-item{
	@apply flex justify-center items-center flex-col h-fit
}

.header-item{
	@apply flex gap-2 flex-col 2xl:flex-row justify-center items-center
}

</style>
