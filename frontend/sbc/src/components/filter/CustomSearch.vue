<template>
	<div class="flex flex-col items-center">
		<div class="flex justify-center gap-4 p-4">
			<form>
			<input class="border-2 border-gray-700 rounded-md text-black text-center p-2" v-model="searchField"/>
				<ul class="max-h-48 overflow-y-auto min-w-48 overflow-x-hidden">
					<li v-for="option in options" class="autoCompleteItem text-center text-base" @click="()=>select(option)">
						{{option}}
					</li>
				</ul>
			</form>
			<span><button @click="add">Add</button></span>
		</div>
		<h3 class="text-black font-semibold justify-center flex text-lg pb-2" v-if="selectedItems.length > 0 ">Selected Items:</h3>
		<ul class="overflow-y-auto max-h-48 min-w-48" >
			<li v-for="item in selectedItems" class="flex gap-4 items-center justify-start p-2">
				<button @click="del(item)"><Delete/></button><div class="text-black">{{item}}</div>
			</li>
		</ul>
	</div>
</template>

<script setup lang="js">
import {useCbcStore} from "../../lib/stores/CbcStore.js";
import {computed, ref, watch} from "vue";
import Delete from "../icons/Delete.vue";
import {useModalStore} from "../../lib/stores/ModalStore.js";

const searchField = ref("")
watch(searchField, (value)=>{
	if(value.includes(",")) searchField.value = searchField.value.replace(",", ".")
})

const cbcStore = useCbcStore()
const modalStore = useModalStore()
const filterKey = computed(()=> modalStore.getFilterKey)
const selectedItems = computed(
	{
		get() {
			return modalStore.getSelectedItemsFromFilter
		}
	}
)
const options = computed(()=>{
	if(filterKey.value === undefined) return []
	const filterKeyValues = cbcStore.getCbcMeasurements.map(cbc => cbc[filterKey.value])
	const filteredOptions = filterKeyValues.filter(value => {
		if(value === undefined) return false
		return value.toString().toLowerCase().includes(searchField.value.toString().toLocaleLowerCase())
	})
	const excludeSelectedItemsOptions = filteredOptions.filter(value => !selectedItems.value.includes(value))
	return Array.from(new Set(excludeSelectedItemsOptions))
})

function add(){
	modalStore.addSelectedItemToFilter(searchField.value)
}

function del(item){
	modalStore.removeItemFromFilter(item)
}

function select(option){
	searchField.value = option
	add()
	searchField.value = ""
}

watch(filterKey, ()=>{
	searchField.value = ""
})
</script>

<style scoped>

</style>
