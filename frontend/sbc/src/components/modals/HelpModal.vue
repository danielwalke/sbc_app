<template>
	<div :class="isOpen ? 'block' : 'hidden' " id="default-modal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50
	 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
		<div class="relative p-4 w-full max-w-2xl max-h-full">
			<!-- Modal content -->
			<div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
				<!-- Modal header -->
				<div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
					<h3 class="text-xl font-semibold text-gray-900 dark:text-white">
						{{headerContent}}
					</h3>
					<button @click="close" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="default-modal">
						X
					</button>
				</div>
				<!-- Modal body -->
				<div class="p-4 md:p-5 space-y-4">
					<div class="text-base leading-relaxed text-gray-500 dark:text-gray-400" v-html="mainContent">
					</div>
				</div>
				<!-- Modal footer -->
				<div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
					<button @click="close" data-modal-hide="default-modal" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
						Okay
					</button>
				</div>
			</div>
		</div>
	</div>

</template>

<script setup lang="js">
import {useModalStore} from "../../lib/stores/ModalStore.js";
import {computed} from "vue";

const store = useModalStore()

const isOpen = computed(()=> store.getIsHelpModalOpen)
const headerContent = computed(()=> store.getHeaderContent)
const mainContent = computed(()=> store.getHelpMainContent)

function close(){
	store.setIsHelpModalOpen(false)
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  margin: 20px;
  color: #333;
}
h1, h2 {
  color: #0056b3;
}
p {
  margin-bottom: 1em;
}
.highlight {
  font-weight: bold;
  color: #d9534f;
}
ul {
  margin-left: 20px;
  list-style-type: square;
}
</style>
