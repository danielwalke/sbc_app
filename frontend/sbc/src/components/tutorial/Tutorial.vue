<script setup>
import { VideoPlayer } from '@videojs-player/vue'
import 'video.js/dist/video-js.css'
import ImportData from "../../assets/import_data.mov"
import SubmitData from "../../assets/submit_data.mov"
import DataImport from "./contents/DataImport.js";
import {ref} from "vue";

function scrollToSection(){
  const targetElement = document.getElementById("start");
  if(targetElement === null) return
  targetElement.scrollIntoView(
      {
        behavior: 'smooth',
        block: 'start'
      }
  )
};

const currSlide = ref(0)

const titleDict = {
  "DataImport": "Importing data (CSV)",
  "SubmitData": "Submitting data",
}

const videoDict = {
  "DataImport": ImportData,
  "SubmitData": SubmitData,
}

const contentDict = {
  "DataImport": DataImport
}

const slideTitles = Object.keys(titleDict)

function nextVideo(){
  currSlide.value += 1
}

function prevVideo(){
  currSlide.value -= 1
}
</script>

<template>
  <div class="w-full h-full pt-4 pl-4 pb-4 select-none" id="startTutorial">
    <div class="w-full h-[90%] flex justify-start items-center flex-col ">
      <div class="header mb-8 p-2 text-center text-lg lg:text-2xl font-semibold">{{titleDict[slideTitles[currSlide]]}}</div>
      <div class="w-full lg:w-3/5 lg:text-xl h-4/5 video-container flex gap-4 items-center">
        <div class=" h-[10%] animate-bounce-left text-white text-4xl flex justify-center cursor-pointer" @click="prevVideo" v-if="currSlide > 0">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 32 24" stroke-width="3" stroke="currentColor" class="w-10 h-10">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l-10 7m0 0l10 7M14 12H29" />
          </svg>
        </div>
        <div class="text-container" v-html="contentDict[slideTitles[currSlide]]">
        </div>
        <video-player
            :src="videoDict[slideTitles[currSlide]]"
            controls
            :loop="true"
            :volume="0.0"
            autoplay="muted"
        />
        <div class=" h-[10%] animate-bounce-right text-white text-4xl flex justify-center cursor-pointer" @click="nextVideo" v-if="currSlide < slideTitles.length -1">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 32 24" stroke-width="3" stroke="currentColor" class="w-10 h-10">
            <path stroke-linecap="round" stroke-linejoin="round" d="M18 5l10 7m0 0l-10 7M18 12H3" />
          </svg>
        </div>
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
.video-container >>> .video-js {
  height: 100%;
  width: 100%;
}

/* Or, for older Vue versions */
.video-container /deep/ .video-js {
  height: 100%;
  width: 100%;
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

.animate-bounce-right {
  animation: bounce-right 1.5s infinite;
}

@keyframes bounce-right {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(10px);
  }
}

.animate-bounce-left {
  animation: bounce-left 1.5s infinite;
}

@keyframes bounce-left {
  0%, 100% {
    transform: translateX(0px);
  }
  50% {
    transform: translateX(-10px);
  }
}

.text-container {
  @apply text-xl font-semibold
}
::v-deep(.text-container > div > ol > li) {
  @apply p-2;
}

</style>