<script setup>
import { VideoPlayer } from '@videojs-player/vue'
import 'video.js/dist/video-js.css'
import ImportData from "../../assets/tutorial/ImportSmallData.mov"
import SubmitData from "../../assets/tutorial/AnalysisType.mov"
import Home from "../../assets/tutorial/Home.mov"
import Sensitivity from "../../assets/tutorial/Sensitivity.mov"
import ShapValues from "../../assets/tutorial/ShapValues.mov"
import OtherModels from "../../assets/tutorial/OtherModels.mov"
import Sorting from "../../assets/tutorial/Sorting.mov"
import SingleInput from "../../assets/tutorial/SingleInput.mov"
import ShapValuesSeries from "../../assets/tutorial/ShapValuesSeries.mov"
import Filter from "../../assets/tutorial/Filter.mov"
import FilterInTimeSeries from "../../assets/tutorial/FilterInTimeSeries.mov"
import DataImportContent from "./contents/DataImport.js";
import SubmitDataContent from "./contents/SubmitData.js";
import SingleInputContent from "./contents/SingleInput.js"
import SortingContent from "./contents/Sorting.js"
import ShapValuesContent from "./contents/ShapValues.js"
import ShapValuesTimeSeriesContent from "./contents/ShapTimeSeries.js"
import FilterContent from "./contents/Filter.js"
import FilterTimeSeriesContent from "./contents/FilterTimeSeries.js";
import SensitivityContent from "./contents/Sensitivity.js"
import HomeContent from "./contents/Home.js"
import OtherModelsContent from "./contents/OtherModels.js"
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
}

const currSlide = ref(0)

const titleDict = {
  "DataImport": "Importing data (CSV)",
  "SingleInput": "Add single measurement",
  "SubmitData": "Selecting analysis type & submitting data",
  "Sorting": "Sort data",
  "ShapValues": "Investigate SHAP-values",
  "ShapValuesSeries": "Investigate SHAP-values of measurements in a time-series",
  "Filter": "Filter data",
  "FilterInTimeSeries": "Filter data in time-series",
  "Sensitivity": "Customize sensitivity",
  "OtherModels": "Investigate further machine learning models",
  "Home": "Reset everything"
}

const videoDict = {
  "DataImport": ImportData,
  "SubmitData": SubmitData,
  "ShapValues": ShapValues,
  "ShapValuesSeries": ShapValuesSeries,
  "Filter": Filter,
  "FilterInTimeSeries": FilterInTimeSeries,
  "Sensitivity": Sensitivity,
  "SingleInput": SingleInput,
  "OtherModels": OtherModels,
  "Sorting": Sorting,
  "Home": Home
}

const contentDict = {
  "DataImport": DataImportContent,
  "SubmitData": SubmitDataContent,
  "SingleInput": SingleInputContent,
  "Sorting": SortingContent,
  "ShapValues": ShapValuesContent,
  "ShapValuesSeries": ShapValuesTimeSeriesContent,
  "FilterInTimeSeries": FilterTimeSeriesContent,
  "Filter": FilterContent,
  "Sensitivity": SensitivityContent,
  "Home": HomeContent,
  "OtherModels": OtherModelsContent
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
  <div class="w-full h-full pl-2 lg:pt-4 lg:pl-4 lg:pb-4 select-none" id="startTutorial">
    <div class="w-full h-[90%] flex justify-start items-center flex-col ">
      <div class="header mb-2 lg:mb-8 lg:p-2 text-center text-lg lg:text-2xl font-semibold">{{titleDict[slideTitles[currSlide]]}}</div>
      <div class="w-[94%] lg:w-[97%] lg:text-xl h-4/5 video-container flex gap-8 items-center">

        <div class=" h-[10%] animate-bounce-left text-white text-4xl flex justify-center cursor-pointer" @click="prevVideo" v-if="currSlide > 0">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 32 24" stroke-width="3" stroke="currentColor" class="w-10 h-10">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l-10 7m0 0l10 7M14 12H29" />
          </svg>
        </div>

        <div class="w-full h-full flex items-center justify-center lg:flex-row flex-col gap-4">
        <div class="text-container" v-html="contentDict[slideTitles[currSlide]]"></div>

        <video-player
            :src="videoDict[slideTitles[currSlide]]"
            controls
            :loop="true"
            :volume="0.0"
            autoplay="muted"
        />
        </div>

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
::v-deep(.video-js) {
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
    transform: translateX(-10px);
  }
  50% {
    transform: translateX(-20px);
  }
}

.text-container {
  @apply text-sm md:text-base lg:text-xl font-semibold text-justify
}
::v-deep(li) {
  @apply lg:p-2 leading-none lg:leading-6 p-1;
}

</style>