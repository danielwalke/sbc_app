from service.meta.CBC import CBC


class LLMInput(CBC):
    pred_proba: float
    risk: float
    shap_age: float
    shap_sex: float
    shap_WBC: float
    shap_PLT: float
    shap_RBC: float
    shap_MCV: float
    shap_HGB: float
