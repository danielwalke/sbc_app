<template>
  <div :class="isOpen ? 'block' : 'hidden' " id="default-modal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-2
	 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div class="relative p-4 w-full max-w-2xl max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            Customize sensitivity
          </h3>
          <button @click="close" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="default-modal">
            X
          </button>
        </div>
        <!-- Modal body -->
        <div class="p-4 md:p-5 space-y-4">
          <form class="flex gap-2 justify-center">
            <input type="checkbox" id="check_best" class="w-4" v-model="isBestThresholdSelected"/>
            <label for="check_best" class="text-black">Optimal threshold based on ROC</label>
          </form>

          <div class="relative">
            <div v-if="isBestThresholdSelected" class=" absolute inset-0 flex items-center justify-center z-50">
              <div class="bg-gray-300 text-red-600 p-2 rounded-md">Disabled if checkbox selected</div>
            </div>
            <div :class="isBestThresholdSelected ? 'opacity-30' : 'opacity-100' " class="p-4">
              <Slider  :disabled="isBestThresholdSelected" v-model="rangeValues" :min="0" :max="100" :classes="{
  target: 'relative box-border select-none touch-none tap-highlight-transparent touch-callout-none disabled:cursor-not-allowed',
  focused: 'slider-focused',
  tooltipFocus: 'slider-tooltip-focus',
  tooltipDrag: 'slider-tooltip-drag',
  ltr: 'slider-ltr',
  rtl: 'slider-rtl',
  horizontal: 'slider-horizontal h-1.5',
  textDirectionRtl: 'slider-txt-rtl',
  textDirectionLtr: 'slider-txt-ltr',
  base: 'w-full h-full relative z-1 bg-gray-300 rounded',
  connects: 'w-full h-full relative overflow-hidden z-0 rounded',
  connect: 'absolute z-1 top-0 right-0 transform-origin-0 transform-style-flat h-full w-full bg-sky-700 cursor-pointer tap:duration-300 tap:transition-transform disabled:bg-gray-400 disabled:cursor-not-allowed',
  origin: 'slider-origin absolute z-1 top-0 right-0 transform-origin-0 transform-style-flat h-full w-full h:h-0 v:-top-full txt-rtl-h:left-0 txt-rtl-h:right-auto v:w-0 tap:duration-300 tap:transition-transform',
  handle: 'absolute rounded-full bg-white border-0 shadow-slider cursor-grab focus:outline-none h:w-4 h:h-4 h:-top-1.5 h:-right-2 txt-rtl-h:-left-2 txt-rtl-h:right-auto v:w-4 v:h-4 v:-top-2 v:-right-1.25 disabled:cursor-not-allowed focus:ring focus:ring-sky-700 focus:ring-opacity-30',
  handleLower: 'slider-hande-lower',
  handleUpper: 'slider-hande-upper',
  touchArea: 'h-full w-full',
  tooltip: 'absolute block text-sm font-semibold whitespace-nowrap py-1 px-1.5 min-w-5 text-center text-white rounded border border-sky-700 bg-sky-700 transform h:-translate-x-1/2 h:left-1/2 v:-translate-y-1/2 v:top-1/2 disabled:bg-gray-400 disabled:border-gray-400 merge-h:translate-x-1/2 merge-h:left-auto merge-v:-translate-x-4 merge-v:top-auto tt-focus:hidden tt-focused:block tt-drag:hidden tt-dragging:block',
  tooltipTop: 'bottom-6 h:arrow-bottom merge-h:bottom-3.5',
  tooltipBottom: 'top-6 h:arrow-top merge-h:top-5',
  tooltipLeft: 'right-6 v:arrow-right merge-v:right-1',
  tooltipRight: 'left-6 v:arrow-left merge-v:left-7',
  tooltipHidden: 'slider-tooltip-hidden',
  active: 'slider-active shadow-slider-active cursor-grabbing',
  draggable: 'cursor-ew-resize v:cursor-ns-resize',
  tap: 'slider-state-tap',
  drag: 'slider-state-drag'
}"/>
            </div>

          </div>
        </div>
        <!-- Modal footer -->
        <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
          <button @click="close" data-modal-hide="default-modal" >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="js">
import {useModalStore} from "../../lib/stores/ModalStore.js";
import {computed, ref, watch} from "vue";
import {useCbcStore} from "../../lib/stores/CbcStore.js";
import Slider from '@vueform/slider'
import {submitCbcMeasurements} from "../../lib/api/CBCPredcitions.js";


const store = useModalStore()
const cbcStore = useCbcStore()
const isBestThresholdSelected = ref(true)

const isOpen = computed(()=> store.getIsSensitivityModelOpen)

const rangeValues = computed({
  get() {
    if(cbcStore.getMinSensitivity === undefined) return 0
    return cbcStore.getMinSensitivity
  },
  set(value) {
    cbcStore.setMinSensitivity(value)
    submitCbcMeasurements()
  }
})

function close(){
  store.setIsSensitivityModelOpen(false)
}

function selectBestThreshold(){
  cbcStore.setMinSensitivity(undefined)
}

watch(isBestThresholdSelected, (newVal, oldVal) => {
  if(newVal){
    cbcStore.setMinSensitivity(undefined)
    return submitCbcMeasurements()
  }
  cbcStore.setMinSensitivity(80)
  submitCbcMeasurements()

})
</script>

<style scoped>
.disabled\:opacity-50 {
  opacity: 0.5;
}

.disabled\:filter-grayscale {
  filter: grayscale(1);
}
</style>

