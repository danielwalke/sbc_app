<template>
    <label for="file-input">
        File Upload
    </label>
    <input type="file" id="file-input" multiple @change="onInputChange" />

</template>

<script setup>
const props = defineProps({
    onInputChange:Function
})

</script>

<style scoped>

</style>