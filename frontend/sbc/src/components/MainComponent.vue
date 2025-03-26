<template>
	<div class="w-full custom-height pt-2">
    <div class="overflow-y-auto w-full h-full">
      <Introduction/>
      <Tutorial/>
      <SBCShap/>
    </div>
	</div>
</template>

<script setup>
import SBCShap from "./SBCShap.vue";
import Introduction from "./Introduction.vue";
import Tutorial from "./tutorial/Tutorial.vue";
</script>

<style scoped>
</style>
