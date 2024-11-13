<template>
	<div class="w-full custom-height pt-4 pl-4 pb-4">
		<Header/>
		<Content/>
		<SubmitContainer/>
	</div>
</template>

<script setup>
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import Content from "./header/input/Content.vue";
import Header from "./header/Header.vue";
import SubmitContainer from "./submit/SubmitContainer.vue";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
</script>

<style scoped>
</style>
