export function addTimeSeriesData(state, filteredCbcMeasurements){
    if(!state.addTimeSeriesData) return filteredCbcMeasurements
    const filteredPatientIds = filteredCbcMeasurements.map(cbc => cbc.patientId)
    const filteredUuids = filteredCbcMeasurements.map(cbc => cbc.id)
    const timeSeriesData = state.cbcMeasurements.filter(cbc => filteredPatientIds.includes(cbc.patientId) && !filteredUuids.includes(cbc.id))
    filteredCbcMeasurements.push(...timeSeriesData)
    return filteredCbcMeasurements
}