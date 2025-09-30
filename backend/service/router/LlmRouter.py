from fastapi import APIRouter, Request
from service.constants.Server import ADD_PATH
from service.meta.LLMInput import LLMInput
import os
import requests
import json
import hashlib

router = APIRouter(redirect_slashes=False)

@router.post(ADD_PATH + "/llm_resp")
async def get_llm_shap_response(request: Request, body:LLMInput):
    prompt = f"""
            You are an expert AI assistant for clinicians, specializing in making machine learning predictions understandable. Your task is to explain a sepsis risk prediction based on a patient's complete blood count (CBC) data.
            
            You will be provided with the patient's lab values, the model's risk score, and the SHAP values explaining the prediction. Use the hardcoded clinical reference ranges below to interpret the patient's data.
            
            **Your Explanation Must:**
            1.  Begin with a direct, one-sentence summary of the model's sepsis risk prediction.
            2.  Explain the contribution of the most important features to this prediction.
            3.  For each feature, **you must compare the patient's value to the provided clinical reference range**. Clearly state if the value is low, normal, or high. Highlight most important information in bold (markdown).
            4.  Directly link this status (e.g., "high white blood cell count") to its impact on the risk score (e.g., "...which was the primary factor that increased the predicted risk.").
            5.  Use clear, accessible language and structure the output as a single, coherent narrative in markdown.
            
            ---
            
            **Patient Inputs:**
            - Age: {body.age}
            - Sex: {body.sex}
            - Hemoglobin (HGB): {body.HGB} mmol/l
            - White Blood Cell Count (WBC): {body.WBC} x10^9/L
            - Red Blood Cell Count (RBC): {body.RBC} x10^12/L
            - Mean Corpuscular Volume (MCV): {body.MCV} fL
            - Platelet Count (PLT): {body.PLT} x10^9/L
            
            **Clinical Reference Ranges:**
            - HGB Range: 7.14 - 11.05 mmol/l
            - WBC Range: 3.7 - 11.5 x10^9/L
            - RBC Range: 4.1 - 5.9 x10^12/L
            - MCV Range: 80 - 96 fL
            - PLT Range: 137 - 443 x10^9/L
            
            **Model Outputs:**
            - Predicted Sepsis Risk: {body.risk} %
            
            **SHAP Values (Feature Contributions):**
            - Age: {body.shap_age}
            - Sex: {body.shap_sex}
            - HGB: {body.shap_HGB}
            - WBC: {body.shap_WBC}
            - RBC: {body.shap_RBC}
            - MCV: {body.shap_MCV}
            - PLT: {body.shap_PLT}
            
            ---
            
            Please generate the clinical explanation now.
    """
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    if prompt_hash in request.app.state.llm_cache:
        print(f"Total tokens used: 0 (used the cache)")
        return request.app.state.llm_cache[prompt_hash]
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": request.app.state.API_KEY,
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    llm_answer = response['candidates'][0]['content']['parts'][0]['text']
    total_tokens = response['usageMetadata']['totalTokenCount']
    print(f"Total tokens used: {total_tokens}")
    print(llm_answer)
    request.app.state.llm_cache[prompt_hash] = llm_answer
    return llm_answer