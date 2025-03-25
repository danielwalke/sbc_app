<script setup>
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import Content from "./header/input/Content.vue";
import Header from "./header/Header.vue";
import SubmitContainer from "./submit/SubmitContainer.vue";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
</script>

<template>
  <div class="w-full h-full" id="start">
    <Header/>
    <Content/>
    <SubmitContainer/>
  </div>
</template>

<style scoped>

</style>