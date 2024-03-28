export function calculate_confidence_score(class_probability, threshold = 0.5){
	let m
	let n
	if(class_probability <= threshold){
		m = - 1 / threshold
		n = 1
	}else{
		m = 1 / (1-threshold)
		n = - threshold * m
	}
	const confidence = m*class_probability+n
	return confidence
}
