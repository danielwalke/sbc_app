<template>

	<div :class="isOpen ? 'block' : 'hidden' " id="default-modal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-2
	 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
		<div class="relative p-4 w-full max-w-2xl max-h-full">
			<!-- Modal content -->
			<div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
				<!-- Modal header -->
				<div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
					<h3 class="text-xl font-semibold text-gray-900 dark:text-white">
						Add new data
					</h3>
					<button @click="close" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="default-modal">
						X
					</button>
				</div>
				<!-- Modal body -->
				<div class="p-4 md:p-5 space-y-4 flex justify-center flex-col items-center gap-2">
					<div class="flex justify-center items-center">
						<FileInput />
					</div>
					<div class="flex justify-center w-full mt-4">
						<button
							@click="addCbcMeasurement">
							New Row
						</button>
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
import FileInput from "../header/input/FileInput.vue";
import {DEFAULT_CBC} from "../../lib/constants/CBC_Constants.js";
import {useCbcStore} from "../../lib/stores/CbcStore.js";
import {computed} from "vue";
import {useModalStore} from "../../lib/stores/ModalStore.js";


const store = useCbcStore()
const modalStore = useModalStore()

function addCbcMeasurement(){
	store.unshiftCbcMeasurements({...DEFAULT_CBC})
	close()
}

const isOpen = computed(()=> modalStore.getIsInputModelOpen)

function close(){
	modalStore.setIsInputModalOpen(false)
}
</script>

<style scoped>

</style>
