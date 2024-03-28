export function getAUROCOutput(state){
	const groundTruthList = state.getCbcMeasurements.map(cbc => cbc.groundTruth)
	if(groundTruthList.some(y => y === undefined)) return "Calculation without ground-truth not possible"
	if(new Set(groundTruthList).size === 1) return "Calculation for only one label not possible"
	return Math.round(state.auroc * 10000) / 10000
}
