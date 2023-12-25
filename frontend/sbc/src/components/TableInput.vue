<template>
    <FileInput :onInputChange="onInputChange"/>
  <div class="w-full grid leading-6 pt-2 gap-4 pl-4 pr-4" :class="pred_proba === undefined ? 'grid-cols-8':'grid-cols-10'" v-for="(cbc, idx) in cbcs">
    <div v-for="cbcKey in cbcKeys" class="flex justify-center items-center flex-col h-fit">
      <p class="text-center">{{cbcKey}}</p>
      <p class="text-center">({{unit(cbcKey)}})</p>
      <input
          class="p-2 rounded-md w-full w-32 text-right" :value="cbc[cbcKey]"
          :type="type(cbcKey)"
          :placeholder="cbcKey"
          @input="event => valueInput(event, cbc, cbcKey)">
    </div>
    <ResultColumnProba v-if="pred_proba && pred_proba[idx] !== undefined" title="Probability sepsis" :value="pred_proba[idx]" />
    <ResultColumnPred v-if="pred && pred[idx] !== undefined" title="Prediction" :value="pred[idx]"/>
    <div class="col-span-1" v-if="shaps.length>0"></div>
      <div class="col-span-7 flex justify-center max-h-48" v-if="chartData && chartData[idx]">
        <Bar :data="chartData[idx]" :options="options"/>
      </div>
</div>

  <div>
  <div class="flex justify-center w-full mt-4"><button
      @click="()=> cbcs.push({...cbc})"
      class="flex justify-center items-center rounded-full border-2 text-white h-fit w-fit p-4 text-2xl pt-2 pb-2">+</button></div>
  <SubmitButton :submit="submit"/>
</div>
</template>

<script setup>
import {computed, ref} from "vue";
import axios from "axios";
import {PORT, SERVER_URL} from "../lib/constants/Server.js";
import { Bar } from 'vue-chartjs'
import ResultColumnProba from "./results/ResultColumnProba.vue";
import ResultColumnPred from "./results/ResultColumnPred.vue";
import SubmitButton from "./results/SubmitButton.vue";
import FileInput from "./input/FileInput.vue";
import {DEFAULT_CBC, UNITS_DICT} from "../lib/constants/CBC_Constants.js";
import {chartOptions} from "../lib/constants/ChartOptions.js";
import Chart from 'chart.js/auto';
//TODO Input Validation + Refactoring + solve rendering problem
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const cbc = DEFAULT_CBC
const options = chartOptions

const shaps = ref([])
const cbcs  = ref([{...cbc}])
const pred_proba = ref(undefined)
const pred = ref(undefined)
const chartData= computed(
    {
        get() {

            if(shaps.value.length === 0) return undefined
            return shaps.value.map((shaps_value_item) => ({
                labels: Object.keys(cbc).slice(1, Object.keys(cbc).length),
                datasets: [{ backgroundColor: shaps_value_item.map(s => s<= 0 ? "blue" : "red"),fontColor:"white",data: shaps_value_item }]
            }))
        },
        set(newValue) {
            shaps.value = newValue
        }
    })

function unit(cbcKey){
  return UNITS_DICT[cbcKey]
}

function type(cbcKey){return cbcKey === "sex" ? "text" : "number"}


const cbcKeys = computed(() => {
  return Object.keys(cbc)
})


function valueInput(event, cbc, cbcKey){
  if(cbcKey === "sex") return cbc[cbcKey] = event.target.value
  cbc[cbcKey] = +event.target.value
}

function submit(){
  axios.post(SERVER_URL + 'get_pred', cbcs.value)
      .then(function (response) {
        pred_proba.value = response.data.pred_probas
        pred.value = response.data.predictions
        chartData.value = response.data.shap_values
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
            if(line.length===0) continue
            if(lineIdx==0) continue
            const items = line.split(";")
            cbcs.value.push({
                patientId: items[0],
                age: +items[1],
                sex: items[2],
                HGB: +items[3],
                WBC: +items[4],
                RBC: +items[5],
                MCV: +items[6],
                PLT: +items[7],

            })
        }
    };
    reader.readAsText(file);
}
</script>

<style scoped>

</style>