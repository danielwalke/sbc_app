import {routes} from "./Routes.js";
import { createRouter, createWebHistory } from "vue-router";
import {useCbcStore} from "../stores/CbcStore.js";

export const router = createRouter({
	history: createWebHistory(),
	routes,
})
router.beforeEach((to, from, next) => {


	if (to.path === "/sbc_frontend") {
		const cbcStore = useCbcStore()
		cbcStore.setHasPredictionDetails(undefined)
	}
	next()
})
