<template>
  <div class="relative">
    <!-- Dropdown trigger button -->
    <button
        @click="toggleDropdown"
        class="flex items-center justify-between w-48 px-4 py-2 bg-sky-700 text-white rounded-md shadow-sm hover:bg-sky-800 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 transition-colors duration-200"
        aria-haspopup="true"
        :aria-expanded="isOpen"
    >
      <span>{{ selectedOption || placeholder }}</span>
      <svg
          class="w-5 h-5 ml-2 transition-transform duration-200"
          :class="{ 'transform rotate-180': isOpen }"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
      >
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>

    <!-- Dropdown menu -->
    <div
        v-if="isOpen"
        class="absolute z-10 w-48 mt-1 bg-sky-700 border border-sky-600 rounded-md shadow-lg"
    >
      <ul
          class="py-1"
          role="menu"
          aria-orientation="vertical"
      >
        <li
            v-for="option in options"
            :key="option.value"
            @click="selectOption(option)"
            class="px-4 py-2 text-sm text-white hover:bg-sky-800 cursor-pointer transition-colors duration-150"
            role="menuitem"
        >
          {{ option.label }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount, computed} from 'vue'
import {useCbcStore} from "../../../lib/stores/CbcStore.js";

const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  }
})

const emit = defineEmits(['select'])
const store = useCbcStore()

const isOpen = ref(false)
const selectedOption = computed(()=>store.getPredictionType)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  store.setPredictionType(option.value)
  isOpen.value = false
  emit('select', option.value)

}

const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  selectOption({
    "label": "prospective",
    "value": "prospective",
  })
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>