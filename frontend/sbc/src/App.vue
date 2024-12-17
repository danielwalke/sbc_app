<script setup>
import HelpModal from "./components/modals/HelpModal.vue";
import FilterModal from "./components/modals/FilterModal.vue";
import LoadingSkeleton from "./components/loader/LoadingSkeleton.vue";
import {useCbcStore} from "./lib/stores/CbcStore.js";
import Footer from "./components/footer/Footer.vue";
import InputModal from "./components/modals/InputModal.vue";
import {fetchClassifierNamesAndThresholds} from "./lib/api/ClassifierInitialization.js";
import SensitivityModal from "./components/modals/SensitivityModal.vue";


const cbcStore = useCbcStore()
fetchClassifierNamesAndThresholds()
</script>

<template>
  <div class="h-screen w-screen min-h-[640px] overflow-y-auto">
		<router-view></router-view>
		<HelpModal/>
		<FilterModal/>
		<LoadingSkeleton/>
    <SensitivityModal/>
		<InputModal/>
		<Footer/>
  </div>
</template>

<style scoped>

</style>
