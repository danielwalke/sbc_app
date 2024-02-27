<script setup>
import HelpModal from "./components/modals/HelpModal.vue";
import FilterModal from "./components/modals/FilterModal.vue";
import LoadingSkeleton from "./components/loader/LoadingSkeleton.vue";

</script>

<template>
  <div class="h-screen w-screen">
		<router-view></router-view>
		<HelpModal/>
		<FilterModal/>
		<LoadingSkeleton/>
  </div>
</template>

<style scoped>

</style>
