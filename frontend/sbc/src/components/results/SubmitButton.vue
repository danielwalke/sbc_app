<template>
    <div class="flex justify-center w-full mt-4">
        <button class="rounded-md border-2 text-white p-4 shadow-md hover:bg-gray-800" @click="submit">Submit</button>
    </div>
</template>

<script setup>
const props = defineProps({
    submit:Function
})

</script>

<style scoped>

</style>