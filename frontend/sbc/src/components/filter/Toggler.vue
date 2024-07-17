<script setup lang="js">
import {computed, ref} from 'vue'
import {useCbcStore} from "../../stores/CbcStore.js";
import Help from "../icons/Help.vue";
import LiddleClose from "../icons/LiddleClose.vue";

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

const isHelpOpen = ref(false)
</script>

<template>
	<div class=" flex justify-center gap-2">
		<div class="bg-gray-300 flex justify-center  items-center p-2 rounded-md bg-sky-700" >
			<label class="flex cursor-pointer select-none items-center">
				<div class="relative">
					<input type="checkbox" class="sr-only" @change="handleCheckboxChange" />
					<div :class="{ 'bg-[#18A101]': isChecked, 'bg-[#374151]': !isChecked }" class="block h-8 w-14 rounded-full"></div>
					<div
						:class="{ 'translate-x-full bg-sky-700': isChecked }"
						class="dot absolute left-1 top-1 h-6 w-6 rounded-full bg-white transition"
					></div>
				</div>
			</label>
			<div class="bg-sky-700 p-4 gap-2 rounded-md flex justify-center">
				<div class="text-white font-semibold text-center ">Include Time series data</div>
				<Help @click="isHelpOpen = !isHelpOpen"/>
			</div>
		</div>
		<div v-if="isHelpOpen" class="max-w-48 overflow-y-auto max-h-20 bg-sky-700 rounded-md pt-2">
			<LiddleClose @click="isHelpOpen = !isHelpOpen"/>
			<div class="pl-4 pr-4 pb-2">Adds all samples of a time series if one sample in the time series matches the filter criteria</div>
		</div>
	</div>

</template>
