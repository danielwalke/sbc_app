<script setup>
import HelpModal from "./components/modals/HelpModal.vue";
import FilterModal from "./components/modals/FilterModal.vue";
import LoadingSkeleton from "./components/loader/LoadingSkeleton.vue";
import {useCbcStore} from "./stores/CbcStore.js";
import Footer from "./components/footer/Footer.vue";
import InputModal from "./components/modals/InputModal.vue";


const cbcStore = useCbcStore()
cbcStore.fetchClassifierNames()
</script>

<template>
  <div class="h-screen w-screen min-h-[640px] overflow-y-auto">
		<router-view></router-view>
		<HelpModal/>
		<FilterModal/>
		<LoadingSkeleton/>
		<InputModal/>
		<Footer/>
  </div>
</template>

<style scoped>

</style>
