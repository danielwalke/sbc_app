<template>
<div>
  <button @click="()=> isOpen = !isOpen" id="dropdownDefaultButton" data-dropdown-toggle="dropdown" class="text-white bg-sky-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center hover:bg-sky-600 focus:bg-sky-600" type="button">
    {{selectedFilterValue ? selectedFilterValue : "Sample-Filter"}}
    <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
    </svg>
  </button>

  <!-- Dropdown menu -->
  <div :class="isOpen? '' : 'hidden'" class="z-10 bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700">
    <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownDefaultButton">
      <li v-for="value in values" @click="()=> handleValueSelection(value)">
        <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
          {{value}}
        </a>
      </li>
    </ul>
  </div>
</div>
</template>

<script setup>
import {computed, ref} from "vue";
import {FALSE_NEGATIVE, FALSE_POSITIVE, TRUE_NEGATIVE, TRUE_POSITIVE} from "../lib/constants/FilterOptions.js";
import {useCbcStore} from "../stores/CbcStore.js";
const isOpen = ref(false)

function handleValueSelection(value){
	store.setSelectedFilterValue(value)
  isOpen.value = !isOpen.value
}
const store = useCbcStore()
const selectedFilterValue = computed(()=>store.getSelectedFilterValue)

const values = [TRUE_POSITIVE, TRUE_NEGATIVE, FALSE_POSITIVE, FALSE_NEGATIVE]

</script>

<style scoped>

</style>
