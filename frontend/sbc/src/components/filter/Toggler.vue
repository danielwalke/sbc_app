<script setup lang="js">
import {computed, ref} from 'vue'
import {useCbcStore} from "../../stores/CbcStore.js";

const store = useCbcStore()
const isChecked = computed({
	get(){
		return store.getAddTimeSeriesData
	},
	set(val){
		store.setAddTimeSeriesData(val)
	}
})

const handleCheckboxChange = () => {
	isChecked.value = !isChecked.value
}
</script>

<template>
	<div class="flex gap-4 justify-center items-center">
		<label class="flex cursor-pointer select-none items-center">
			<div class="relative">
				<input type="checkbox" class="sr-only" @change="handleCheckboxChange" />
				<div :class="{ 'bg-sky-700': isChecked, 'bg-[#E5E7EB]': !isChecked }" class="block h-8 w-14 rounded-full"></div>
				<div
					:class="{ 'translate-x-full bg-sky-700': isChecked }"
					class="dot absolute left-1 top-1 h-6 w-6 rounded-full bg-white transition"
				></div>
			</div>
		</label>
		<div class="text-black font-semibold text-center">Include Time series data</div>
	</div>

</template>
