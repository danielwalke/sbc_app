<template>
<div>
  <div v-for="cbcKey in cbcKeys">
    <input :value="cbc[cbcKey]"
           :type="type(cbcKey)"
           :placeholder="cbcKey"
           @input="event => cbc[cbcKey] = event.target.value"><div>{{unit(cbcKey)}}</div>
  </div>
  <button @click="submit">Submit</button>
</div>
</template>

<script setup>

import {computed, ref} from "vue";
import axios from "axios";
import {PORT, SERVER_URL} from "../constants/Server.js";

const cbc = ref({
  patientId: 0,
  age: 18,
  sex: "W",
  HGB: 10,
  RBC: 8,
  WBC: 10,
  MCV: 30,
  PLT: 24,

})

function unit(cbcKey){
  const units = {
    patientId: "identifier",
    age:"years",
    sex:"binary (W/M)",
    HGB: "mmol/l",
    WBC: "Gpt/l",
    RBC: "Gpt/l",
    MCV: "fl",
    PLT: "Gpt/l"
  }
  return units[cbcKey]
}

function type(cbcKey){
  if(cbcKey === "sex") return "text"
  return "number"
}

const cbcKeys = computed(() => {
  //parse as numbers
  return Object.keys(cbc.value)
})




function submit(){
  for(const cbcKey in cbc.value){
    if(cbcKey === "sex") cbc.value[cbcKey] = cbc.value[cbcKey] === "W" ? 1  : 0
    cbc.value[cbcKey] = +cbc.value[cbcKey]
  }
  axios.post(SERVER_URL + 'cbc_measurement', cbc.value)
      .then(function (response) {
        console.log(response);
      })
}
</script>

<style scoped>

</style>