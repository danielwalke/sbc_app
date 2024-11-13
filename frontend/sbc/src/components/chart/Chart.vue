<template>
	<td class="col-span-7 flex flex-col pt-4 pb-4 justify-center max-h-48 align-center" v-if="cbc.chartData">
		<div class="flex gap-2 justify-center font-semibold">
			<div>SHAP-values</div><div class="text-red-600">Sepsis</div><div>vs.</div><div class="text-blue-600">Control</div>
		</div>
		<Bar :data="cbc.chartData[shapType]" :options="chartOptions"/>
	</td>
</template>

<script setup lang="js">
import { Bar } from 'vue-chartjs'
import {chartOptions} from "../../lib/constants/ChartOptions.js";

const props = defineProps({
	cbc:Object,
  shapType:String,
})
</script>

<style scoped>

</style>
