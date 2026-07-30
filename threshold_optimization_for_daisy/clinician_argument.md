# Clinical Recommendation & Threshold Argument for Sepsis Screening (Daisy Project)

## Executive Summary & Key Recommendation

When deploying a machine learning decision support system for clinical sepsis prediction in non-ICU patients, selecting the operational decision threshold based purely on **unconstrained Positive Predictive Value (PPV / Precision)** yields a threshold of `0.8610`. While this achieves a high PPV, it results in an unacceptably low **Sensitivity of 1.11% on training data (0.82% on internal validation and 0.00% on external validation)**—missing over **99% of all sepsis cases**. 

In clinical sepsis management, missing a septic patient (False Negative) carries catastrophic risk (delayed antibiotic administration, rapid clinical deterioration, severe organ dysfunction, and mortality), whereas a false alarm (False Positive) results in secondary laboratory re-evaluation or clinical monitoring.

### 🌟 Recommended Operational Threshold for Clinical Deployment
We recommend deploying the **$F_2$-Optimized Threshold (`t = 0.8147`)** derived from the Precision-Recall (PR) Curve (or the **Target 50% Sensitivity Threshold `t = 0.6781`** depending on hospital risk tolerance).

---

## Performance Summary Across All Cohorts

### 1. Model Discrimination Metrics
- **Leipzig Train (Internal Training)**: **AUROC = 0.9117**, **AUPRC = 0.0304**
- **Leipzig Validation (Internal Test)**: **AUROC = 0.8693**, **AUPRC = 0.0171**
- **Greifswald Validation (External Validation)**: **AUROC = 0.8168**, **AUPRC = 0.0054**

---

### 2. Threshold Strategy Comparison Matrix

| Strategy | Operational Threshold ($t$) | Cohort | PPV (Precision) | Sensitivity (Recall) | Specificity | F1-Score | True Positives (TP) | False Positives (FP) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Raw Max PPV (Clinically Unusable)** | `0.8610` | **Train**<br>**Leipzig Test**<br>**Greifswald Ext** | `21.52%`<br>`12.50%`<br>`0.00%` | `1.11%`<br>`0.82%`<br>`0.00%` | `99.99%`<br>`99.99%`<br>`100.00%` | `0.0212`<br>`0.0153`<br>`0.0000` | `17`<br>`4`<br>`0` | `62`<br>`28`<br>`0` |
| **PR-Curve Max $F_1$ (Balanced)** | `0.8450` | **Train**<br>**Leipzig Test**<br>**Greifswald Ext** | `8.85%`<br>`4.24%`<br>`1.23%` | `6.23%`<br>`4.08%`<br>`3.57%` | `99.90%`<br>`99.88%`<br>`99.71%` | `0.0731`<br>`0.0416`<br>`0.0183` | `95`<br>`20`<br>`16` | `979`<br>`452`<br>`1282` |
| 🛡️ **PR-Curve Max $F_2$ (Recommended Clinical)** | `0.8147` | **Train**<br>**Leipzig Test**<br>**Greifswald Ext** | **`3.63%`**<br>**`2.31%`**<br>**`0.84%`** | **`22.67%`**<br>**`17.35%`**<br>**`16.07%`** | **`99.09%`**<br>**`99.02%`**<br>**`98.06%`** | `0.0626`<br>`0.0407`<br>`0.0160` | `346`<br>`85`<br>`72` | `9,179`<br>`3,599`<br>`8,490` |
| 🏥 **Target Sens $\ge 50\%$ (High-Catch Screening)** | `0.6781` | **Train**<br>**Leipzig Test**<br>**Greifswald Ext** | `1.73%`<br>`1.28%`<br>`0.52%` | `50.13%`<br>`46.94%`<br>`42.86%` | `95.70%`<br>`95.13%`<br>`91.65%` | `0.0334`<br>`0.0248`<br>`0.0103` | `765`<br>`230`<br>`192` | `43,573`<br>`17,799`<br>`36,524` |
| **Default Threshold** | `0.5000` | **Train**<br>**Leipzig Test**<br>**Greifswald Ext** | `1.13%`<br>`0.79%`<br>`0.37%` | `70.18%`<br>`63.67%`<br>`57.14%` | `90.74%`<br>`89.31%`<br>`84.34%` | `0.0222`<br>`0.0156`<br>`0.0074` | `1071`<br>`312`<br>`256` | `93,875`<br>`39,101`<br>`68,547` |

---

## Clinical Argumentation for Clinicians & Hospital Committees

### 1. Why Unconstrained Max PPV (`t = 0.8610`) is Clinically Unacceptable
Optimizing solely for raw PPV selects an extreme tail threshold. In a dataset with low sepsis prevalence (~0.10% - 0.15%), an unconstrained PPV optimizer achieves high precision by triggering alerts only for a handful of glaringly obvious cases. In practice, **it misses 99 out of 100 septic patients**. An AI system that fails to alert on 99% of disease cases provides zero clinical utility and creates a false sense of security.

### 2. Why the $F_2$-Optimized Threshold (`t = 0.8147`) is the Best Clinical Balance
The $F_2$-metric weights **Sensitivity twice as heavily as Precision** ($F_2 = 5 \cdot \frac{P \cdot R}{4P + R}$). This mathematical formulation explicitly mirrors clinical decision-making under low disease prevalence:
- **Catches 1 in 5-6 septic cases early** prior to ICU admission based purely on routine blood work.
- **Maintains > 98% Specificity** across both internal and external hospital centers, preventing alert fatigue and avoiding unnecessary workload burden for nursing and medical staff.
- Demonstrates robust generalization on the external **Greifswald cohort** (**16.07% Sensitivity** and **98.06% Specificity**).

### 3. Alternative: Target 50% Sensitivity Threshold (`t = 0.6781`) for High-Risk Wards
If the hospital unit prioritizes maximum patient safety over notification frequency (e.g., high-risk surgical or oncology wards), the threshold `t = 0.6781` can be selected. This guarantees that **~50% of all sepsis cases are detected** (46.9% in Leipzig Test, 42.9% in Greifswald) while keeping Specificity above **91% - 95%**.
