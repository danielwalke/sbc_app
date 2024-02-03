export const DEFAULT_CBC = {
    patientId: 0,
    age: 18,
    sex: "W",
    HGB: 9,
    WBC: 4,
    RBC: 5,
    MCV: 80,
    PLT: 500,
    groundTruth: undefined,
    pred: undefined,
    pred_proba: undefined,

}

export const UNITS_DICT = {
    patientId: "identifier",
    age:"years",
    sex:"binary (W/M)",
    HGB: "mmol/l",
    WBC: "Gpt/l",
    RBC: "Gpt/l",
    MCV: "fl",
    PLT: "Gpt/l"
}