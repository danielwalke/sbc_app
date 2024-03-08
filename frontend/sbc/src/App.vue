<script setup>
import HelpModal from "./components/modals/HelpModal.vue";
import FilterModal from "./components/modals/FilterModal.vue";
import LoadingSkeleton from "./components/loader/LoadingSkeleton.vue";
import {useCbcStore} from "./stores/CbcStore.js";
import Footer from "./components/footer/Footer.vue";


const cbcStore = useCbcStore()
cbcStore.fetchClassifierNames()
</script>

<template>
  <div class="h-screen w-screen">
		<router-view></router-view>
		<HelpModal/>
		<FilterModal/>
		<LoadingSkeleton/>
		<Footer/>
  </div>
</template>

<style scoped>

</style>
