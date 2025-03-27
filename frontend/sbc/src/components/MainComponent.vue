<template>
	<div class="w-full custom-height pt-4">
    <div class="overflow-y-auto w-full h-full" @scroll="handleScroll">
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
import {useModalStore} from "../lib/stores/ModalStore.js";

const modalStore = useModalStore()
function handleScroll(){
  modalStore.setIsScrolled(true)
}
</script>

<style scoped>
</style>
