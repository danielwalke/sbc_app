<template>
	<div class="custom-height w-full absolute z-10 top-0 left-0 overflow-hidden" :class="isLoading ? 'block':'hidden' " style="background-color: #242424">
		<div class="p-4">
			<div class="flex justify-center w-full pb-3">
				<div class="non-editable skeleton max-w-40"></div>
			</div>
			<div class="w-full overflow-x-auto max-h-[80%]">
				<table class="table-auto min-w-[1300px] h-full relative w-full">
				<TableHeader :is-detail-page="false"/>
				<tbody class="w-full grid leading-6 pt-2 gap-4 grid-container"
						 v-for="_ in 15" >
					<td v-for="_ in editableCbcKeys" class="flex justify-center items-center flex-col h-fit">
						<div
							class="p-2 rounded-md w-full w-32 h-12 text-right text-black skeleton-bright"></div>
					</td>
					<td class="non-editable skeleton"></td>
					<td class="flex justify-between col-span-3 gap-4">
						<div class="non-editable skeleton"></div>
						<div class="non-editable skeleton"></div>
						<div class="non-editable skeleton"></div>
					</td>

					<td class="col-span-2 " ></td>
					<td class="col-span-7 flex justify-center max-h-48">
						<div class="skeleton"></div>
					</td>
				</tbody>
				</table>
			</div>
			<div class="flex justify-center w-full">
				<div class="non-editable skeleton max-w-40"></div>
			</div>
		</div>
	</div>
</template>

<script setup lang="js">
import {editableCbcKeys} from "../../lib/TableGrid.js"
import {useCbcStore} from "../../stores/CbcStore.js";
import {computed} from "vue";
import TableHeader from "../input/TableHeader.vue";

const cbcStore = useCbcStore()
const isLoading = computed(()=>cbcStore.getIsLoading)
</script>

<style scoped>


.skeleton{
	animation: skeleton-loading 1s linear infinite reverse;
	opacity: .7;
}

.skeleton-bright{
	animation: skeleton-bright-loading 1s linear infinite reverse;
	opacity: .7;
}


.grid-container {
	display: grid;
	grid-template-columns: repeat(13, minmax(0, 1fr));
	gap: 1rem;
}

.non-editable{
	@apply p-2 bg-gray-600 rounded-md w-full text-center select-none h-12
}


@keyframes icon-loading {
	0%{
		color: hsl(200, 20%, 70%);
	}
	100%{
		color: hsl(200, 20%, 95%);
	}
}

@keyframes skeleton-loading {
	0%{
		background-color: hsl(200, 20%, 70%);
	}
	100%{
		background-color: hsl(200, 20%, 85%);
	}
}

@keyframes skeleton-bright-loading {
	0%{
		background-color: hsl(200, 20%, 80%);
	}
	100%{
		background-color: hsl(200, 20%, 99%);
	}
}
</style>
