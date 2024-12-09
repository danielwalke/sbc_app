import RiskOverview from "../../assets/Sepsis risk.drawio.svg"

export const CBC_KEY_TO_DESCRIPTION = {
	age: "age in years",
	HGB: "hemoglobin in milli-mole per liter",
	WBC: "white blood cells in giga-particles per liter",
	RBC: "red blood cells in tera-particles per liter",
	MCV: "mean corpuscular volume in femto-liter",
	PLT: "platelets in giga-particles per liter",
	order: "Time measurement order for a single patient",
	patientId: "Anonymous numeric identifier for a patient",
	groundTruth: "Ground-truth value of the specified instance",
	confidence: "<div class=' max-h-[70vh] overflow-y-auto'>" +
		"<div></div>" +
		"<h1 class=\"text-lg font-bold text-sky-600 mb-4\">Sepsis Risk Prediction</h1>\n" +
		"    <p class=\"mb-4\">\n" +
		"        Machine learning classifiers return prediction probabilities between \n" +
		"        <span class=\"font-bold text-red-600\">zero (\"Control\")</span> and \n" +
		"        <span class=\"font-bold text-red-600\">one (\"Sepsis\")</span>. However, these prediction probabilities \n" +
		"        do not incorporate prevalence information \n" +
		"        <span class=\"italic\">(i.e., sepsis is less frequent than controls)</span>.\n" +
		"    </p>\n" +
		"    <p class=\"mb-4\">\n" +
		"        Therefore, if we were to use a threshold of \n" +
		"        <span class=\"font-bold text-red-600\">0.5</span> to calculate the sepsis risk, many sepsis cases would remain undetected due to their low prevalence.\n" +
		"    </p>\n" +
		"    <h2 class=\"text-lg font-semibold text-sky-600 mb-3\">Incorporating Prevalence Information</h2>\n" +
		"    <p class=\"mb-4\">\n" +
		"        To incorporate prevalence information, we can calculate an optimal threshold \n" +
		"        (<span class=\"font-bold text-red-600\">Fig. 1 A</span>) based on the Receiver Operating Curve \n" +
		"        <span class=\"italic\">(e.g., threshold with the largest Geometric Mean)</span>.\n" +
		"    </p>\n" +
		"    <p class=\"mb-4\">The process involves:</p>\n" +
		"    <ul class=\"list-disc list-inside mb-4\">\n" +
		"        <li class=\"mb-2\">Calculating two linear regressions:</li>\n" +
		"        <ul class=\"list-circle list-inside ml-6 mb-4\">\n" +
		"            <li class=\"mb-1\">One from <span class=\"font-bold text-red-600\">zero</span> to the optimal threshold.</li>\n" +
		"            <li>Another from the threshold to <span class=\"font-bold text-red-600\">one</span>.</li>\n" +
		"        </ul>\n" +
		"        <li>Using the slopes of these regressions along with previously calculated prediction probabilities.</li>\n" +
		"    </ul>\n" +
		"    <p class=\"mb-4\">\n" +
		"        Based on these steps, we can calculate the sepsis risks \n" +
		"        (<span class=\"font-bold text-red-600\">Fig. 1 B</span>) that also incorporate prevalence information. As a result, we obtain sepsis risks in % from 0 % to 100 % to describe how confident a classifier is in the prediction</p>" +
		`
		<figure class="mt-4">
          <img src="${RiskOverview}" alt="Overview Figure" class="mt-4 rounded-lg shadow-lg p-2">
          <figcaption class="mt-2 text-sm text-gray-500">
            <bold class='font-semibold'>Figure 1: Overview of the sepsis prediction.</bold> 
            First, we calculate an optimal threshold using the Receiver Operating Crev (A). Then, this threshold is used combined with prediction probabilities from machine elarning classifiers to calculate sepsis risks (B).  
          </figcaption>
        </figure>` +
		"</div>",
	pred: "Prediction for the instance with the given classifier",
	classifier: "Classifier used for the classification (default is Random Forest Classifier)",
	sex: "Biological sex (character as 'M' for male or 'W' for female)",
	details: "Click to get results from all classifiers and SHAP-values",

}
