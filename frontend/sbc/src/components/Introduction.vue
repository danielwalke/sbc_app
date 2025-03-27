<script setup>
import {ref, onMounted, computed} from 'vue';
import {useModalStore} from "../lib/stores/ModalStore.js";

// const fullText = "The goal of this app is to predict a potential sepsis event based on a patient's age, sex and " +
//     "complete blood count data (hemoglobin, mean corpuscular volume, white blood cells, red blood cells and platelets)." +
//     " Therefore, users (e.g., clinicians) only need to input these information and submit data to retrieve a potential" +
//     " sepsis. risk. Additionally, we provide insights into the inner-working of the machine ";

const fullTexts = [
    "Real-time prediction of sepsis",
    "Only requires age, sex and complete blood count information",
    "Interpretability of machine learning using SHAP values to see how predictions were made",
    "Multiple machine learning models"
]
const displayedTexts = ref(fullTexts.map(() => ""));
const modalStore = useModalStore()
const isScrolled = computed(()=> modalStore.getIsScrolled)

onMounted(() => {
  let listIndex = 0;
  let charIndex = 0;
  const interval = setInterval(() => {
    if (listIndex < fullTexts.length) {
      if (charIndex < fullTexts[listIndex].length) {
        displayedTexts.value[listIndex] += fullTexts[listIndex][charIndex];
        charIndex++;
      } else {
        listIndex++;
        charIndex = 0;
      }
    } else {
      clearInterval(interval);
      if(isScrolled) return
      setTimeout(()=>{
        scrollToSection()
      }, 500)
    }
  }, 50);
});



function scrollToSection(){
  const targetElement = document.getElementById("startTutorial");
  if(targetElement === null) return
  targetElement.scrollIntoView(
      {
        behavior: 'smooth',
        block: 'start'
      }
  )
}



</script>

<template>
  <div class="w-full h-full pt-4 pl-4 pb-4 select-none">
    <div class="w-full h-[90%] flex justify-center items-center flex-col ">
      <div class="header mb-8 p-2 text-center">SBC-SHAP: Predicting sepsis using interpretable machine learning on complete blood count data</div>
      <div class="w-full lg:w-3/5 lg:text-xl">
        <ul class="text-justify list-disc pl-12">
          <li class="p-2" v-for="(item, index) in displayedTexts" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>

    <div class=" h-[10%] animate-bounce text-white text-4xl flex justify-center cursor-pointer" @click="scrollToSection">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 32" stroke-width="3" stroke="currentColor" class="w-10 h-10">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 18l-7 10m0 0l-7-10m7 10V3" />
      </svg>
    </div>
  </div>
</template>

<style scoped>
.header{
  @apply text-lg md:text-2xl lg:text-4xl;
}

.animate-bounce {
  animation: bounce 1.5s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(10px);
  }
}
</style>