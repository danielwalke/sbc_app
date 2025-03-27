# SBC-SHAP
# SBC-SHAP: Sepsis Risk Prediction System

## Project Overview
SBC-SHAP is an advanced machine learning solution designed to predict interpretable sepsis risk using minimal patient information (sex, age, complete blood count information).

## Key Features

### 1. Real-time Prediction of Sepsis
- Provides immediate risk assessment for sepsis
- Enables early intervention and critical medical decision-making
- Designed to support healthcare professionals in time-sensitive scenarios

### 2. Minimal Input Requirements
- Only requires three key patient data points:
  - Age
  - Sex
  - Complete Blood Count (CBC) information
- Reduces complexity of data collection
- Makes the prediction model accessible and easy to implement

### 3. Advanced Interpretability with SHAP Values
- Utilizes SHAP (SHapley Additive exPlanations) methodology
- Provides transparent insight into how predictions are made
- Allows medical professionals to understand the reasoning behind each risk assessment
- Breaks down the contribution of individual features to the final prediction

### 4. Multiple Machine Learning Models
- Incorporates diverse machine learning algorithms:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - XGBoost
- Enables comprehensive and robust risk prediction
- Allows comparison and validation across different modeling approaches

## Getting Started
For easy access just visit http://daniel-walke.com/sbc-shap.  However, you can also setup everything locally using [Link to my_file.txt](https://github.com/danielwalke/sbc_app/blob/main/docker-compose.yml)](docker-compose) or by cloning this repository and executing the following steps:

```bash
https://github.com/danielwalke/sbc_app.git
```

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

# YouTube Tutorials
## Video Guides
1. [Introduction](https://www.youtube.com/embed/mFxcSfSPRqE?si=bEX_jaI35hjWxA4I)
2. [Input new Data](https://www.youtube.com/embed/MAZnUR2NAtE?si=ta7Z6hLE-vMXifmm)
3. [Input data as CSV](https://www.youtube.com/embed/ltawHl3CHTs?si=1waaawz9zkJ8Cwz5)
4. [Structure of the CSV file](https://www.youtube.com/embed/luiYG8DT59I?si=wyh2IOf08B6IWOOY)
5. [Test data as demonstration](https://www.youtube.com/embed/25aA9UL8NgA?si=m0kEYFKZqvdR_XVs)
6. [Prediction goal](https://www.youtube.com/embed/rxclOvnYKnM?si=z7bM1crXtRq_Pc0T)
7. [Sorting data](https://www.youtube.com/embed/WYnEV6rXWLY?si=v0iIogOf4QaucyNQ)
8. [Filter data](https://www.youtube.com/embed/Ou6TyFyCBac?si=zDlXK1wTmIxI1KrT)
9. [Filter data II (Time-series filtering)](https://www.youtube.com/embed/7An7GzHydnE?si=EqCTF1eOxr2y0xIs)
10. [Customize sensitivity](https://www.youtube.com/embed/xALGYqCN2I8?si=7V9YQWZGagMI3jmy)
11. [Investigate details (SHAP values)](https://www.youtube.com/embed/ymOUin-xRJE?si=mpt-Qbl36c9n5HIe)
12. [Prediction of other classifiers](https://www.youtube.com/embed/WF_Z7rHrdJY?si=qUJjhnLCKyrvkMnj)
13. [Local setup](https://www.youtube.com/embed/qcQakg9_8qQ?si=_EzJU9dMlknlO3uy)


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
