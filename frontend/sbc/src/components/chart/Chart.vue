<template>
	<td class="col-span-7 flex flex-col pt-4 pb-4 justify-center max-h-48 align-center" v-if="cbc.chartData">
		<div class="flex gap-2 justify-center font-semibold">
			<div>SHAP-values</div><div class="text-red-600">Sepsis</div><div>vs.</div><div class="text-blue-600">Control</div> <Help :fun="() => helpSHAP()"/>
		</div>
		<Bar :data="cbc.chartData[shapType]" :options="chartOptions"/>
	</td>
</template>

<script setup lang="js">
import { Bar } from 'vue-chartjs'
import {chartOptions} from "../../lib/constants/ChartOptions.js";
import {CBC_KEY_TO_DESCRIPTION} from "../../lib/constants/CBCDescriptions.js";
import Help from "../icons/Help.vue";
import {useModalStore} from "../../lib/stores/ModalStore.js";

const props = defineProps({
	cbc:Object,
  shapType:String,
})

const modalStore = useModalStore()

function helpSHAP(){
  const content =
      "<div class=' max-h-[70vh] overflow-y-auto'>" +
      "<div></div>" +
      "    <p class=\"mb-4 text-justify\">\n" +
      "        SHAP-values show how a specific value of a feature/attribute (e.g., white blood cells) changes the predicted sepsis risk. Specifically, <span class=\"font-bold text-red-600\">positive SHAP-values (red)</span> indicate that this feature value increased the predicted sepsis risk.\n" +
      "        On the other hand, a <span class=\"font-bold text-sky-600\">negative SHAP-value (blue) </span> indicate that this feature value decreases the sepsis risk. The <span class=\"font-bold\">magnitude</span> of the SHAP-value show the importance of this feature value to the predicted sepsis risk. <span class=\"font-bold\">Larger magintudes</span> indicate a <span class=\"font-bold\">high importance</span> to the predicted risk and <span class=\"font-bold\">low magnitudes</span> (i.e., near zero) indicate a <span class=\"font-bold\">low importance</span>."
      "</div>"
  modalStore.setIsHelpModalOpen(true)
  modalStore.setHeaderContent("SHAP-values")
  modalStore.setHelpMainContent(content)
}
</script>

<style scoped>

</style>
