import axios from "axios";
import {ENDPOINT_LLM_EXPLANATION} from "../constants/Server.js";
import {useModalStore} from "../stores/ModalStore.js";

export async function receiveLlmExplanation(cbc){
    console.log(cbc)
    console.log(cbc.chartData["combined"])
    const modalStore = useModalStore()
    modalStore.setLLMResponseLoading(true)
    const data = {
        age: cbc.age,
        sex: cbc.sex,
        HGB: cbc.HGB,
        WBC: cbc.WBC,
        RBC: cbc.RBC,
        MCV: cbc.MCV,
        PLT: cbc.PLT,
        ground_truth: undefined,
        pred_proba: cbc.pred_proba,
        risk: cbc.confidence,
        shap_age: cbc.chartData["combined"].datasets[0].data[0],
        shap_sex: cbc.chartData["combined"].datasets[0].data[1],
        shap_WBC: cbc.chartData["combined"].datasets[0].data[2],
        shap_PLT: cbc.chartData["combined"].datasets[0].data[3],
        shap_RBC: cbc.chartData["combined"].datasets[0].data[4],
        shap_MCV: cbc.chartData["combined"].datasets[0].data[5],
        shap_HGB: cbc.chartData["combined"].datasets[0].data[6],
    };
    console.warn(data)
    try{
        const resp = await axios.post(ENDPOINT_LLM_EXPLANATION, data,{
            timeout: 120000 // Timeout set to 10 seconds
        })
        console.log(resp.data)
        modalStore.setLLMResponse(resp.data)
        modalStore.setLLMResponseLoading(false)
        modalStore.setIsExplanationModalOpen(true)
    }catch(e){
        console.error(e);
    }


}