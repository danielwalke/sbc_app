import {computed} from "vue";
import {DEFAULT_CBC} from "./constants/CBC_Constants.js";

export const editableCbcKeys = computed(() => {
	return Object.keys(DEFAULT_CBC).filter(key => !["groundTruth", "pred", "pred_proba", "cbc_data"].includes(key))
})
