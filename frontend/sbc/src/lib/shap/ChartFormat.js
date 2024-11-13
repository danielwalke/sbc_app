export function getShapFormat(shapValues){
    const labels = ["age", "sex", "HGB", "WBC", "RBC", "MCV", "PLT"]
    return {
        labels: labels,
        datasets: [{ backgroundColor: shapValues.map(s => s<= 0 ? "#2563eb" : "#dc2626"),fontColor:"white",data: shapValues}]
    }
}