import {parseFile} from "./FileParser.js";

export function readCbcFile(file){
    const reader = new FileReader();
    reader.onload = (res) => {
        parseFile(res.target.result)
    };
    reader.readAsText(file);
}