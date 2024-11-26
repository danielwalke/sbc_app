<template>
<div class="h-12 text-black flex items-center justify-center bg-gray-700">
	<div class="flex gap-8 overflow-hidden text-xs md:text-sm lg:text-base">
		<router-link to="/sbc_frontend" class="route">Main-App</router-link>
		<router-link to="/sbc_frontend/disclaimer" class="route">Disclaimer</router-link>
		<router-link to="/sbc_frontend/about" class="route">Impressum</router-link>
	</div>
</div>
</template>

<script setup lang="ts">
import {useRoute, useRouter} from "vue-router";

const route = useRoute()
const router = useRouter()
</script>

<style scoped>
.route{
	@apply p-2 cursor-pointer rounded-md text-white hover:scale-110
}
</style>
