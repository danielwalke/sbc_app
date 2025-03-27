<template>
  <div class="h-12 text-black flex items-center justify-center bg-gray-700 w-full overflow-x-auto">
    <div class="pl-32 flex gap-4 lg:gap-8 text-xs md:text-sm lg:text-base min-w-max">
      <router-link to="/sbc-shap" class="route">Main-App</router-link>
      <router-link to="/yt-tutorials" class="route">YT-Tutorials</router-link>
      <router-link to="/sbc-shap/disclaimer" class="route">Disclaimer</router-link>
      <router-link to="/sbc-shap/about" class="route">Impressum</router-link>
      <router-link to="/sbc-shap/data-privacy" class="route">Data privacy</router-link>
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
