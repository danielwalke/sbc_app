export function calculate_confidence_score(class_probability, threshold = 0.5){
    let m
    let n
    if(class_probability <= threshold){
        m = 0.5 / threshold
        n = 0
    }else{
        m = 0.5 / (1- threshold)
        n = 0.5 - m * threshold
    }
    return m * class_probability + n
}