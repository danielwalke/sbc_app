# SBC-SHAP
Web application for predicting sepsis and visualizing SHAP values for increased interpretability.

Requirements:
python>=3.X
node v16.14.0
npm 8.3.1

Install frontend:
```bash
cd frontend/sbc/
npm run install
```

Install backend:
```bash
cd backend
pip install -r .\requirements.txt
```

Run frontend:
```bash
cd frontend/
npm run dev
```


Run backend:
```bash
cd backend/
uvicorn main:app --reload
```
# Data Import
## How to Import Data
1. Click on the blue "Input"-button
2. Click on "New file"
3. Select your file

# Single Input
## How to Add a Single Input
1. Click on the blue Input button
2. Click on the blue 'New Row' button
3. Modify the default values in the respective input-fields

# Sorting
## How to Sort and Filter Data
1. Click on the filter-icon for the respective attribute
2. Choose a specific range or specific values for filtering
3. By enabling on the 'Include Time series data'-toggle you retrieve the complete time-series that contains a measurement with the selected filter

# Submit Data
## How to Submit and Analyze Data
1. Click on the help-icon (?) if you need a description of the different analysis modes
2. Select the respective analysis mode form the drop-down menu (prospective (ref.) is recommended)
3. Investigate the predictions

# Sensitivity
## How to Adjust Sensitivity
1. Click on the blue Sensitivity button
2. Unselect the 'Optimal threshold based on ROC' checkbox
3. Select the desired sensitivity value
4. Close the sensitivity window

# SHAP Time Series
## How to View SHAP Values for Time Series
1. Click on the details-icon (magnifier-icon on the right)
2. Investigate SHAP-values
3. 'Sample' shows the influence of the current measurement
4. 'Time' shows the influence of the time-series on the predicted sepsis risk
5. 'Combined' shows the combined influence of the individual measurement and the complete time-series

# SHAP Values
## Understanding SHAP Values
1. Click on the details-icon (magnifier-icon on the right)
2. Investigate SHAP-values
3. Blue values indicate that the attribute (e.g., white blood cells) decrease the sepsis risk. Red values indicate that the attribute increases the sepsis risk.
4. The magnitude indicates how much the attribute changes the sepsis risk. The closer the values are to zero the smaller the influence on the predicted sepsis risk.

# Filter
## How to Filter Data
1. Click on the filter-icon for the respective attribute
2. Choose a specific range with the slider
3. Alternatively, you can select individual values by searching in the input-field and adding the value by clicking on the blue 'Add' button
4. You can remove all filters by clicking on the blue 'Reset Filter' button

# Filter Time Series
## How to Sort Time Series
1. Click on the attribute in the table header to sort based on this attribute
2. Click on further attributes to apply multi-level sorting
3. By clicking on the same attribute multiple times, you can reverse the sorting
4. You can reset all applied sortings by clicking on the blue 'Reset Sort' button

# Other Models
## How to Investigate Other Prediction Models
1. Click on the blue list-icon on the right
2. You can investigate the prediction from the logistic regression, decision tree, random forest and XGBoost
3. You can go back by clicking on the blue arrow on the top left

# Home
## How to Return to Home
1. Click on the blue Home-Icon on the top
