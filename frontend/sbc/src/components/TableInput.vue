<template>
  <div class="flex justify-center items-center p-2 gap-4">
    <FileInput :onInputChange="onInputChange"/>
    <FilterDropdown v-if="has_predictions && cbcs[0].groundTruth !== undefined" :selectedFilterValue="selectedFilterValue" :setSelectedFilterValue="(value)=> selectedFilterValue = value"/>
  </div>
    <Content :cbcs="cbcs" :shaps="shaps"
    :value-input="valueInput" :selectedFilterValue="selectedFilterValue" :has_predictions="has_predictions"/>

  <div>
  <div class="flex justify-center w-full mt-4"><button
      @click="()=> cbcs.push({...cbc})"
      class="flex justify-center items-center rounded-full border-2 text-white h-fit w-fit p-4 text-2xl pt-2 pb-2">+</button></div>
  <SubmitButton :submit="submit" :isLoading="isLoading"/>
</div>
</template>

<script setup>
import {computed, ref} from "vue";
import axios from "axios";
import {SERVER_URL} from "../lib/constants/Server.js";
import SubmitButton from "./results/SubmitButton.vue";
import FileInput from "./input/FileInput.vue";
import {DEFAULT_CBC} from "../lib/constants/CBC_Constants.js";
//TODO Input Validation + Refactoring + solve rendering problem
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import Content from "./Content.vue";
import FilterDropdown from "./FilterDropdown.vue";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const cbc = DEFAULT_CBC
const isLoading = ref(false)
const has_predictions = ref(false)
const selectedFilterValue = ref(undefined)
const shaps = ref([])
const cbcs  = ref([{...cbc}])

function valueInput(event, cbc, cbcKey){
  if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
  cbc[cbcKey] = +event.target.value
}

function submit(){
  isLoading.value = true
  axios.post(SERVER_URL + 'get_pred', cbcs.value.map(c=>({
    patientId: c.patientId,
    age: c.age,
    sex: c.sex,
    HGB: c.HGB,
    WBC: c.WBC,
    RBC: c.RBC,
    MCV: c.MCV,
    PLT: c.PLT,
  })))
      .then(function (response) {
		  isLoading.value = false
        has_predictions.value = true
        for(let i in cbcs.value){
          const cbc = cbcs.value[i]
          cbc.pred = response.data.predictions[i]
          cbc.pred_proba = response.data.pred_probas[i]
			cbc.chartData ={
				labels: Object.keys(cbc).filter(key =>  !["groundTruth", "pred", "pred_proba"].includes(key)).slice(1, Object.keys(cbc).length),
				datasets: [{ backgroundColor: response.data.shap_values[i].map(s => s<= 0 ? "blue" : "red"),fontColor:"white",data: response.data.shap_values[i] }]
			}

        }
      })
}

function onInputChange(e) {
    const file = e.target.files[0]
    const reader = new FileReader();
    let content = null;
    reader.onload = (res) => {
        cbcs.value = []
        content = res.target.result;
        const lines = content.split("\n")
        for(const lineIdx in lines){
            const line = lines[lineIdx]
            if(line.length===0 || lineIdx==0) continue
            const items = line.split(";")
            cbcs.value.push({
                patientId: items[0],
                age: +items[1],
                sex: items[2],
                HGB: Math.round(+items[3]*100)/100,
                WBC: Math.round(+items[4]*100)/100,
                RBC: Math.round(+items[5]*100)/100,
                MCV: Math.round(+items[6]*100)/100,
                PLT: Math.round(+items[7]*100)/100,
              groundTruth: items.length > 8 ? +items[8] === 1 : undefined
            })
        }
    };
    reader.readAsText(file);
}
</script>

<style scoped>

</style>
