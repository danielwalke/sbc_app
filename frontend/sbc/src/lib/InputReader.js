import {v4 as uuid} from "uuid";
import {useCbcStore} from "../stores/CbcStore.js";

export function readCSV(file){
	const store = useCbcStore()
	const reader = new FileReader();
	let content = null;
	reader.onload = (res) => {
		store.setCbcMeasurements([])
		store.setHasPredictions(false)
		content = res.target.result;
		const lines = content.split("\n")
		for(const lineIdx in lines){
			const line = lines[lineIdx]
			if(line.length===0 || lineIdx==0) continue
			const items = line.split(";")
			store.addCbcMeasurements({
				uuid: uuid(),
				patientId: items[0],
				order: +items[1],
				age: +items[2],
				sex: items[3],
				HGB: Math.round(+items[4]*100)/100,
				WBC: Math.round(+items[5]*100)/100,
				RBC: Math.round(+items[6]*100)/100,
				MCV: Math.round(+items[7]*100)/100,
				PLT: Math.round(+items[8]*100)/100,
				groundTruth: items.length > 8 ? +items[9] === 1 ? 'Sepsis' : 'Control' : undefined
			})
		}
	};
	reader.readAsText(file);
}
