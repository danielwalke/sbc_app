from fastapi import APIRouter, Request
from service.constants.Server import ADD_PATH
from service.meta.LLMInput import LLMInput
import os
import requests
import json

router = APIRouter(redirect_slashes=False)

@router.post(ADD_PATH + "/llm_resp")
async def get_llm_shap_response(request: Request, body:LLMInput):
    prompt = f"""
    You are an assistant helping clinicians understand machine learning model explanations using SHAP values.
    The model predicts the risk of sepsis based on complete blood count (CBC) features.

    Here are the patient inputs:
    - Age: {body.age}
    - Sex: {body.sex}
    - Hemoglobin (HGB): {body.HGB}
    - White Blood Cell Count (WBC): {body.WBC}
    - Red Blood Cell Count (RBC): {body.RBC}
    - Mean Corpuscular Volume (MCV): {body.MCV}
    - Platelet Count (PLT): {body.PLT}

    Model outputs:
    - Sepsis risk: {body.risk}

    SHAP values (contribution of each feature to the prediction):
    - Age: {body.shap_age}
    - Sex: {body.shap_sex}
    - HGB: {body.shap_HGB}
    - WBC: {body.shap_WBC}
    - RBC: {body.shap_RBC}
    - MCV: {body.shap_MCV}
    - PLT: {body.shap_PLT}

    Please explain to clinicians, in clear and accessible language, how each input feature contributed to the predicted sepsis risk, based on the SHAP values. Highlight which factors increased the risk and which decreased it, and connect these explanations to clinical intuition wherever possible.
    """
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
    return llm_answer