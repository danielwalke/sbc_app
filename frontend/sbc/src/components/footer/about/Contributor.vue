<template>
<div class="w-4/5 lg:w-3/5">
  <div class="font-semibold">{{name}}</div>
  <a :href="getMailLink">{{mail}}</a>
  <div>{{affiliation}}</div>
  <hr/>
</div>
</template>

<script setup>
import {computed} from "vue";

const props = defineProps({
  name: String,
  mail: String,
  affiliation: String
})

const getMailLink = computed(()=> `mailto:${props.mail}`)

</script>

<style scoped>

</style>