#!/usr/bin/env python3
"""
XGBoost Threshold Optimization & Side-by-Side Comparison with Random Forest (Daisy Project)

This script:
1. Loads the standard XGBoost model and Random Forest model without time series incorporation.
2. Preprocesses the SBC dataset (Leipzig Train, Leipzig Validation Test, and Greifswald External Validation).
3. Computes discrimination metrics (AUROC and AUPRC) for both XGBoost and Random Forest.
4. Performs Precision-Recall (PR) Curve threshold optimization for XGBoost.
5. Evaluates and compares XGBoost vs Random Forest performance across all thresholds and cohorts.
6. Generates diagnostic comparison plots saved in threshold_optimization_for_daisy/xgb_vs_rf_threshold_analysis.png.
"""

import os
import sys
import zipfile
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from joblib import load
from sklearn.metrics import (
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    fbeta_score,
    roc_auc_score,
    average_precision_score,
    roc_curve,
    confusion_matrix,
    ConfusionMatrixDisplay
)

warnings.filterwarnings('ignore')

# Ensure paths are set correctly
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from dataAnalysis.DataAnalysis import DataAnalysis


def print_flush(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def find_sbc_dataset():
    """Locate or extract sbcdata.csv."""
    possible_paths = [
        os.path.join(BACKEND_DIR, "sbcdata.csv"),
        os.path.join(BACKEND_DIR, "extdata", "sbcdata.csv"),
        os.path.join(SCRIPT_DIR, "sbcdata.csv")
    ]
    for p in possible_paths:
        if os.path.isfile(p):
            return p

    zip_path = os.path.join(BACKEND_DIR, "extdata", "sbcdata.zip")
    if os.path.isfile(zip_path):
        print_flush(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(BACKEND_DIR, "extdata"))
        target = os.path.join(BACKEND_DIR, "extdata", "sbcdata.csv")
        if os.path.isfile(target):
            return target

    raise FileNotFoundError("Could not locate sbcdata.csv or sbcdata.zip.")


def load_models():
    """Load both XGBoost and Random Forest standard models."""
    xgb_paths = [
        os.path.join(BACKEND_DIR, "models", "standard", "xgb.joblib"),
        os.path.join(SCRIPT_DIR, "models", "standard", "xgb.joblib")
    ]
    rf_paths = [
        os.path.join(BACKEND_DIR, "models", "standard", "rf.joblib"),
        os.path.join(SCRIPT_DIR, "models", "standard", "rf.joblib")
    ]
    
    xgb_model = None
    rf_model = None
    
    for p in xgb_paths:
        if os.path.isfile(p):
            xgb_model = load(p)
            break
            
    for p in rf_paths:
        if os.path.isfile(p):
            rf_model = load(p)
            break
            
    if xgb_model is None or rf_model is None:
        raise FileNotFoundError("Could not locate xgb.joblib or rf.joblib in models/standard.")
        
    if hasattr(rf_model, 'n_jobs'):
        rf_model.n_jobs = -1
        
    return xgb_model, rf_model


def calculate_metrics(y_true, y_pred):
    """Calculate key binary classification metrics."""
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    ppv = precision_score(y_true, y_pred, zero_division=0)
    sensitivity = recall_score(y_true, y_pred, zero_division=0)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "PPV (%)": ppv * 100,
        "Sensitivity (%)": sensitivity * 100,
        "Specificity (%)": specificity * 100,
        "F1-Score": f1,
    }


def optimize_pr_curve(y_train, y_train_proba):
    """PR Curve Threshold Optimization."""
    precisions, recalls, thresholds = precision_recall_curve(y_train, y_train_proba)
    p, r, t = precisions[:-1], recalls[:-1], thresholds
    
    f1_scores = np.where((p + r) > 0, 2 * (p * r) / (p + r), 0)
    f2_scores = np.where((4 * p + r) > 0, 5 * (p * r) / (4 * p + r), 0)
    
    thresh_df = pd.DataFrame({"Threshold": t, "PPV": p, "Recall": r, "F1": f1_scores, "F2": f2_scores})
    
    t_f1 = t[np.argmax(f1_scores)]
    t_f2 = t[np.argmax(f2_scores)]
    
    mask_50 = r >= 0.50
    t_sens50 = t[mask_50][np.argmax(p[mask_50])] if np.any(mask_50) else 0.50
    
    mask_70 = r >= 0.70
    t_sens70 = t[mask_70][np.argmax(p[mask_70])] if np.any(mask_70) else 0.50
    
    mask_1 = (p > 0) & (r >= 0.01)
    t_raw_ppv = t[mask_1][np.argmax(p[mask_1])] if np.any(mask_1) else t[np.argmax(p)]

    strategies = {
        "Default (0.50)": 0.50,
        "Raw Max PPV (Sens >= 1%)": t_raw_ppv,
        "PR Max F1 (Balanced)": t_f1,
        "PR Max F2 (Clinical Safety)": t_f2,
        "Target Sens >= 50%": t_sens50,
        "Target Sens >= 70%": t_sens70,
    }
    
    return strategies, thresh_df


def main():
    print_flush("=" * 85)
    print_flush("      XGBOOST THRESHOLD OPTIMIZATION & RF COMPARISON (DAISY PROJECT)")
    print_flush("=" * 85)
    
    # 1. Load Models
    print_flush("\n[1/5] Loading XGBoost and Random Forest models...")
    xgb_model, rf_model = load_models()
    print_flush(f"      XGBoost Model: {type(xgb_model).__name__}")
    print_flush(f"      Random Forest Model: {type(rf_model).__name__}")
    
    # 2. Load & Preprocess Data
    dataset_path = find_sbc_dataset()
    print_flush(f"\n[2/5] Loading SBC dataset from:\n      {dataset_path}")
    df_raw = pd.read_csv(dataset_path)
    print_flush(f"      Raw dataset shape: {df_raw.shape}")
    
    print_flush("      Preprocessing dataset using DataAnalysis pipeline...")
    da = DataAnalysis(data=df_raw, print_logs=False)
    
    X_train, y_train = da.get_X_train(), da.get_y_train()
    X_test, y_test   = da.get_X_test(), da.get_y_test()
    X_gw, y_gw       = da.get_X_gw(), da.get_y_gw()
    
    print_flush(f"      Train (Leipzig Train):        {X_train.shape[0]} samples, {y_train.sum()} positives ({y_train.mean()*100:.2f}%)")
    print_flush(f"      Test (Leipzig Validation):    {X_test.shape[0]} samples, {y_test.sum()} positives ({y_test.mean()*100:.2f}%)")
    print_flush(f"      External (Greifswald Valid):  {X_gw.shape[0]} samples, {y_gw.sum()} positives ({y_gw.mean()*100:.2f}%)")
    
    # 3. Model Inference & Discrimination Metrics (AUROC & AUPRC)
    print_flush("\n[3/5] Computing predicted probabilities and discrimination metrics...")
    
    # Predictions
    xgb_train_p = xgb_model.predict_proba(X_train)[:, 1]
    xgb_test_p  = xgb_model.predict_proba(X_test)[:, 1]
    xgb_gw_p    = xgb_model.predict_proba(X_gw)[:, 1]
    
    rf_train_p  = rf_model.predict_proba(X_train)[:, 1]
    rf_test_p   = rf_model.predict_proba(X_test)[:, 1]
    rf_gw_p     = rf_model.predict_proba(X_gw)[:, 1]
    
    discrim_comp = pd.DataFrame([
        {"Dataset": "Leipzig Train", "Model": "XGBoost", "AUROC": roc_auc_score(y_train, xgb_train_p), "AUPRC": average_precision_score(y_train, xgb_train_p)},
        {"Dataset": "Leipzig Train", "Model": "Random Forest", "AUROC": roc_auc_score(y_train, rf_train_p), "AUPRC": average_precision_score(y_train, rf_train_p)},
        {"Dataset": "Leipzig Test",  "Model": "XGBoost", "AUROC": roc_auc_score(y_test, xgb_test_p), "AUPRC": average_precision_score(y_test, xgb_test_p)},
        {"Dataset": "Leipzig Test",  "Model": "Random Forest", "AUROC": roc_auc_score(y_test, rf_test_p), "AUPRC": average_precision_score(y_test, rf_test_p)},
        {"Dataset": "Greifswald Ext", "Model": "XGBoost", "AUROC": roc_auc_score(y_gw, xgb_gw_p), "AUPRC": average_precision_score(y_gw, xgb_gw_p)},
        {"Dataset": "Greifswald Ext", "Model": "Random Forest", "AUROC": roc_auc_score(y_gw, rf_gw_p), "AUPRC": average_precision_score(y_gw, rf_gw_p)},
    ])
    
    print_flush("\n" + "-" * 85)
    print_flush("DISCRIMINATION METRICS COMPARISON (AUROC & AUPRC):")
    print_flush("-" * 85)
    print_flush(discrim_comp.to_string(index=False))
    
    # 4. Threshold Optimization for XGBoost and RF Comparison
    print_flush("\n[4/5] Optimizing thresholds on PR Curve...")
    xgb_strats, xgb_thresh_df = optimize_pr_curve(y_train, xgb_train_p)
    rf_strats, rf_thresh_df   = optimize_pr_curve(y_train, rf_train_p)
    
    def compare_models_on_cohort(cohort_name, y_true, xgb_p, rf_p):
        rows = []
        for s_name in xgb_strats.keys():
            xgb_tr = xgb_strats[s_name]
            rf_tr  = rf_strats[s_name]
            
            xgb_m = calculate_metrics(y_true, (xgb_p >= xgb_tr).astype(int))
            rf_m  = calculate_metrics(y_true, (rf_p >= rf_tr).astype(int))
            
            rows.append({
                "Strategy": s_name,
                "XGB Thresh": xgb_tr,
                "RF Thresh": rf_tr,
                "XGB PPV (%)": xgb_m["PPV (%)"],
                "RF PPV (%)": rf_m["PPV (%)"],
                "XGB Sens (%)": xgb_m["Sensitivity (%)"],
                "RF Sens (%)": rf_m["Sensitivity (%)"],
                "XGB Spec (%)": xgb_m["Specificity (%)"],
                "RF Spec (%)": rf_m["Specificity (%)"],
                "XGB F1": xgb_m["F1-Score"],
                "RF F1": rf_m["F1-Score"],
            })
        return pd.DataFrame(rows)

    train_comp = compare_models_on_cohort("Leipzig Train", y_train, xgb_train_p, rf_train_p)
    test_comp  = compare_models_on_cohort("Leipzig Test", y_test, xgb_test_p, rf_test_p)
    gw_comp    = compare_models_on_cohort("Greifswald Ext", y_gw, xgb_gw_p, rf_gw_p)
    
    print_flush("\n" + "-" * 85)
    print_flush("LEIPZIG TRAIN DATASET: SIDE-BY-SIDE METRICS")
    print_flush("-" * 85)
    print_flush(train_comp[["Strategy", "XGB PPV (%)", "RF PPV (%)", "XGB Sens (%)", "RF Sens (%)", "XGB Spec (%)", "RF Spec (%)", "XGB F1", "RF F1"]].to_string(index=False))

    print_flush("\n" + "-" * 85)
    print_flush("LEIPZIG TEST DATASET (INTERNAL VALIDATION): SIDE-BY-SIDE METRICS")
    print_flush("-" * 85)
    print_flush(test_comp[["Strategy", "XGB PPV (%)", "RF PPV (%)", "XGB Sens (%)", "RF Sens (%)", "XGB Spec (%)", "RF Spec (%)", "XGB F1", "RF F1"]].to_string(index=False))

    print_flush("\n" + "-" * 85)
    print_flush("GREIFSVALD DATASET (EXTERNAL VALIDATION): SIDE-BY-SIDE METRICS")
    print_flush("-" * 85)
    print_flush(gw_comp[["Strategy", "XGB PPV (%)", "RF PPV (%)", "XGB Sens (%)", "RF Sens (%)", "XGB Spec (%)", "RF Spec (%)", "XGB F1", "RF F1"]].to_string(index=False))

    # 5. Save Diagnostic Comparison Plot
    print_flush("\n[5/5] Generating diagnostic comparison plot...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Subplot 1: PR Curves (XGBoost vs RF on Test & Greifswald)
    xgb_pr_p_t, xgb_pr_r_t, _ = precision_recall_curve(y_test, xgb_test_p)
    rf_pr_p_t, rf_pr_r_t, _   = precision_recall_curve(y_test, rf_test_p)
    xgb_pr_p_g, xgb_pr_r_g, _ = precision_recall_curve(y_gw, xgb_gw_p)
    rf_pr_p_g, rf_pr_r_g, _   = precision_recall_curve(y_gw, rf_gw_p)
    
    axes[0, 0].plot(xgb_pr_r_t, xgb_pr_p_t, 'b-', lw=2, label=f"XGB Leipzig Test (AUPRC={average_precision_score(y_test, xgb_test_p):.4f})")
    axes[0, 0].plot(rf_pr_r_t, rf_pr_p_t, 'b--', lw=2, label=f"RF Leipzig Test (AUPRC={average_precision_score(y_test, rf_test_p):.4f})")
    axes[0, 0].plot(xgb_pr_r_g, xgb_pr_p_g, 'r-', lw=2, label=f"XGB Greifswald (AUPRC={average_precision_score(y_gw, xgb_gw_p):.4f})")
    axes[0, 0].plot(rf_pr_r_g, rf_pr_p_g, 'r--', lw=2, label=f"RF Greifswald (AUPRC={average_precision_score(y_gw, rf_gw_p):.4f})")
    axes[0, 0].set_title("Precision-Recall Curves Comparison")
    axes[0, 0].set_xlabel("Recall (Sensitivity)")
    axes[0, 0].set_ylabel("Precision (PPV)")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: ROC Curves (XGBoost vs RF)
    xgb_fpr_t, xgb_tpr_t, _ = roc_curve(y_test, xgb_test_p)
    rf_fpr_t, rf_tpr_t, _   = roc_curve(y_test, rf_test_p)
    xgb_fpr_g, xgb_tpr_g, _ = roc_curve(y_gw, xgb_gw_p)
    rf_fpr_g, rf_tpr_g, _   = roc_curve(y_gw, rf_gw_p)
    
    axes[0, 1].plot(xgb_fpr_t, xgb_tpr_t, 'b-', lw=2, label=f"XGB Leipzig Test (AUROC={roc_auc_score(y_test, xgb_test_p):.4f})")
    axes[0, 1].plot(rf_fpr_t, rf_tpr_t, 'b--', lw=2, label=f"RF Leipzig Test (AUROC={roc_auc_score(y_test, rf_test_p):.4f})")
    axes[0, 1].plot(xgb_fpr_g, xgb_tpr_g, 'r-', lw=2, label=f"XGB Greifswald (AUROC={roc_auc_score(y_gw, xgb_gw_p):.4f})")
    axes[0, 1].plot(rf_fpr_g, rf_tpr_g, 'r--', lw=2, label=f"RF Greifswald (AUROC={roc_auc_score(y_gw, rf_gw_p):.4f})")
    axes[0, 1].plot([0, 1], [0, 1], 'k--', alpha=0.5)
    axes[0, 1].set_title("ROC Curves Comparison")
    axes[0, 1].set_xlabel("False Positive Rate")
    axes[0, 1].set_ylabel("True Positive Rate")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Subplot 3: F2 Score Tradeoff vs Threshold (Train)
    axes[1, 0].plot(xgb_thresh_df["Threshold"], xgb_thresh_df["F2"], 'b-', lw=2, label="XGB F2-Score")
    axes[1, 0].plot(rf_thresh_df["Threshold"], rf_thresh_df["F2"], 'g-', lw=2, label="RF F2-Score")
    axes[1, 0].axvline(xgb_strats["PR Max F2 (Clinical Safety)"], color='blue', linestyle='--', label=f"XGB F2 Thresh ({xgb_strats['PR Max F2 (Clinical Safety)']:.4f})")
    axes[1, 0].axvline(rf_strats["PR Max F2 (Clinical Safety)"], color='green', linestyle=':', label=f"RF F2 Thresh ({rf_strats['PR Max F2 (Clinical Safety)']:.4f})")
    axes[1, 0].set_title("F2-Score Curve vs Threshold (Train)")
    axes[1, 0].set_xlabel("Threshold")
    axes[1, 0].set_ylabel("F2-Score")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Subplot 4: XGBoost Greifswald Confusion Matrix @ Recommended F2 Threshold
    f2_tr_xgb = xgb_strats["PR Max F2 (Clinical Safety)"]
    cm_gw_xgb = confusion_matrix(y_gw, (xgb_gw_p >= f2_tr_xgb).astype(int))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm_gw_xgb, display_labels=["Control", "Sepsis"])
    disp.plot(ax=axes[1, 1], cmap="Purples", values_format="d")
    axes[1, 1].set_title(f"XGBoost Greifswald CM @ F2 Thresh ({f2_tr_xgb:.4f})")
    
    plt.tight_layout()
    plot_out = os.path.join(SCRIPT_DIR, "xgb_vs_rf_threshold_analysis.png")
    plt.savefig(plot_out, dpi=300)
    print_flush(f"      Comparison plot saved to: {plot_out}")
    
    print_flush("\n" + "=" * 85)
    print_flush("XGBOOST VS RF EVALUATION COMPLETE!")
    print_flush("=" * 85)


if __name__ == "__main__":
    main()
