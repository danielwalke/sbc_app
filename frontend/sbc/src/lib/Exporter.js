import {useCbcStore} from "../stores/CbcStore.js";
import {saveAs} from "file-saver";

export function exportCSV(){
	const store = useCbcStore()
	const cbcs = store.getCbcMeasurements
	let output = ""
	if(cbcs.length < 1) return console.alert("Provide enough data")
	const keys = Object.keys(cbcs[0])
	output += keys.join(";")
	output += "\n"
	for(const cbc of cbcs){
		output += Object.values(cbc).join(";")
		output += "\n"
	}

	const blob =  new Blob(new Array(output.trim()), {type: "text/plain;charset=utf-8"});
	saveAs(blob, "ModuleGraph.csv")
}
