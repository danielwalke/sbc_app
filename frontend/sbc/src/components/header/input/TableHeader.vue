<template>
	<thead class="w-full 2xl:max-h-[114px] block top-0 sticky" style="background-color: #242424">
	<tr class="grid-container">
		<th v-for="cbcKey in editableCbcKeys" class="grid-item">
			<div class="header-item pt-2">
				<div class="flex gap-2 text-center hover:cursor-pointer" @click="()=> sortData(cbcKey)">{{cbcKey}}
					<ChevoronUp v-if="sortKey === cbcKey && !sortDirectionReversed"/>
					<ChevronDown v-if="sortKey === cbcKey && sortDirectionReversed"/>
				</div>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction(cbcKey)" :classes="getFilterClass(cbcKey)"/>
				<Help :fun="() => helpCbcKeyFunction(cbcKey)"/>
			</div>
			<p class="text-center">({{unit(cbcKey)}})</p>
		</th>
		<th class="grid-item" >
			<div class="header-item">
				<div class="flex gap-2 text-center hover:cursor-pointer" @click="()=> sortData('groundTruth')">Ground-truth
					<ChevoronUp v-if="sortKey === 'groundTruth' && !sortDirectionReversed"/>
					<ChevronDown v-if="sortKey === 'groundTruth' && sortDirectionReversed"/>
				</div>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('groundTruth')" :classes="getFilterClass('groundTruth')"/>
				<Help :fun="() => helpCbcKeyFunction('groundTruth')"/>
			</div>
		</th>
		<th class="grid-item" >
			<div class="header-item">
				<div class="flex gap-2 text-center hover:cursor-pointer" @click="()=> sortData('confidence')">Sepsis score
					<ChevoronUp v-if="sortKey === 'confidence' && !sortDirectionReversed"/>
					<ChevronDown v-if="sortKey === 'confidence' && sortDirectionReversed"/>
				</div>
				<Filter v-if="!isDetailPage" :fun="()=> filterCbcKeyFunction('confidence')" :classes="getFilterClass('confidence')"/>
				<Help :fun="() => helpCbcKeyFunction('confidence')"/>
			</div>
		</th>
		<th class="header-item" >
			<div class="flex gap-2" v-if="!isDetailPage">
				Details
				<Help :fun="() => helpCbcKeyFunction('details')"/>
			</div>
			<div class="header-item" v-else>
				Classifier
				<Help :fun="() => helpCbcKeyFunction('classifier')"/>
			</div>
		</th>
	</tr>
	</thead>
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

const sortKey = computed(()=> cbcStore.getLastSortKey)
const sortDirectionReversed = computed(()=> cbcStore.getSortDirectionReversed)

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
</script>

<style scoped>
.grid-item{
	@apply flex justify-center items-center flex-col h-fit
}

.header-item{
	@apply flex gap-2 flex-col 2xl:flex-row justify-center items-center
}

</style>
