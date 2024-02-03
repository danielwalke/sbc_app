<template>
    <div class="flex justify-center w-full mt-4">
        <button class="rounded-md shadow-md hover:scale-105 p-4 bg-sky-700 cursor-pointer hover:bg-sky-600" @click="submit">
          {{isLoading ? "Loading..." : "Submit"}}</button>
    </div>
</template>

<script setup>
const props = defineProps({
    submit:Function,
  isLoading:Boolean
})

</script>

<style scoped>

</style>