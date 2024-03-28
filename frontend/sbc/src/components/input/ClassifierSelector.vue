<template>
	<div>
		<form class="max-w-sm mx-auto">
			<select v-model="selectedValue"

							class="bg-sky-700 text-white text-sm rounded-lg focus:ring-blue-500
							 focus:scale-105 block w-full p-4" onfocus="this.size = 5;" onblur="this.size = 0;" onchange="this.size = 1; this.blur();">
				<option type="button" class="option"  v-for="option in allFilterOptions"  :value="option">{{option}}</option>
			</select>
		</form>
	</div>
</template>

<script setup lang="js">
import {computed, ref, watch} from "vue";
import {useCbcStore} from "../../stores/CbcStore.js";

const props = defineProps({
	options: Array
})

const cbcStore = useCbcStore()
const allFilterOptions = computed(()=> cbcStore.getClassifierThresholds ? Object.keys(cbcStore.getClassifierThresholds) : [])

const selectedValue = ref(undefined)

watch(selectedValue, (newSelectedValue) => {
	cbcStore.setDefaultClassifier(newSelectedValue)
})

watch(allFilterOptions, (newOptions) =>{
	selectedValue.value = newOptions[0]
})

</script>

<style scoped>
.option{
	@apply hover:bg-sky-900 cursor-pointer p-2 focus:bg-sky-900 active:bg-sky-900 rounded-md
}
</style>
