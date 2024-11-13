export function getCbcInformation(c){
    return {
        id: c.patientId,
        order: c.order,
        age: c.age,
        sex: c.sex,
        HGB: c.HGB,
        WBC: c.WBC,
        RBC: c.RBC,
        MCV: c.MCV,
        PLT: c.PLT,
        ground_truth: c.groundTruth === "Sepsis" ? 1 : c.groundTruth === "Control"? 0: undefined,
    }
}
