<script setup>
const props = defineProps({
  cbc: Object
})
</script>

<template>
  <div class="col-span-2 flex flex-col gap-2 pt-0 pb-2 pl-2 pr-2">
    <button class="h-14" @click="()=> props.cbc.shapType = 'combined'" :class="props.cbc.shapType === 'combined' ? '' : 'bg-gray-700 hover:bg-gray-600' ">combined</button>
    <button class="h-14" @click="()=> props.cbc.shapType = 'original'" :class="props.cbc.shapType === 'original' ? '' : 'bg-gray-700 hover:bg-gray-600' ">Sample</button>
    <button class="h-14" @click="()=> props.cbc.shapType = 'time'" :class="props.cbc.shapType === 'time' ? '' : 'bg-gray-700 hover:bg-gray-600' ">Time</button>
  </div>
</template>

<style scoped>

</style>