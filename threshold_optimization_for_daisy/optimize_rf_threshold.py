#!/usr/bin/env python3
"""
Random Forest Threshold Optimization for Clinical Deployment (Daisy Project)

This script:
1. Loads the standard Random Forest model (without time series incorporation).
2. Loads and preprocesses SBC dataset (Leipzig Train, Leipzig Validation, and Greifswald External Validation).
3. Computes AUROC and AUPRC (Average Precision) across all three dataset splits.
4. Performs Precision-Recall (PR) Curve based threshold optimization (Max F1, Max F2, and Target Sensitivity >= 50% / >= 70%).
5. Evaluates and compares all threshold strategies on Train, Leipzig Test, and Greifswald External Test.
6. Generates diagnostic plots saved in threshold_optimization_for_daisy/rf_ppv_threshold_analysis.png.
"""

import os
import sys
import zipfile
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
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Ensure backend root is in sys.path
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


def find_rf_model():
    """Locate the Random Forest model without time series incorporation."""
    possible_paths = [
        os.path.join(BACKEND_DIR, "models", "standard", "rf.joblib"),
        os.path.join(SCRIPT_DIR, "models", "standard", "rf.joblib")
    ]
    for p in possible_paths:
        if os.path.isfile(p):
            return p
    raise FileNotFoundError("Could not locate models/standard/rf.joblib.")


def calculate_metrics(y_true, y_pred, y_proba):
    """Calculate key binary classification metrics including AUROC and AUPRC."""
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    ppv = precision_score(y_true, y_pred, zero_division=0)
    sensitivity = recall_score(y_true, y_pred, zero_division=0)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = f1_score(y_true, y_pred, zero_division=0)
    auroc = roc_auc_score(y_true, y_proba)
    auprc = average_precision_score(y_true, y_proba)
    
    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "PPV (Precision)": ppv,
        "Sensitivity (Recall)": sensitivity,
        "Specificity": specificity,
        "F1-Score": f1,
        "AUROC": auroc,
        "AUPRC": auprc
    }


def optimize_pr_curve(y_train, y_train_proba):
    """
    Precision-Recall (PR) Curve based Threshold Optimization.
    Finds thresholds for:
    1. Raw Max PPV
    2. PR-Curve Max F1 Score (Equal weight to PPV and Recall)
    3. PR-Curve Max F2 Score (Recall weighted 2x vs PPV for clinical safety)
    4. Target Sensitivity >= 50%
    5. Target Sensitivity >= 70%
    """
    precisions, recalls, thresholds = precision_recall_curve(y_train, y_train_proba)
    p = precisions[:-1]
    r = recalls[:-1]
    t = thresholds
    
    f1_scores = np.where((p + r) > 0, 2 * (p * r) / (p + r), 0)
    f2_scores = np.where((4 * p + r) > 0, 5 * (p * r) / (4 * p + r), 0)
    
    thresh_df = pd.DataFrame({
        "Threshold": t,
        "PPV": p,
        "Recall": r,
        "F1": f1_scores,
        "F2": f2_scores
    })
    
    # 1. Max F1
    t_f1 = t[np.argmax(f1_scores)]
    
    # 2. Max F2
    t_f2 = t[np.argmax(f2_scores)]
    
    # 3. Target Sensitivity >= 50%
    mask_50 = r >= 0.50
    t_sens50 = t[mask_50][np.argmax(p[mask_50])] if np.any(mask_50) else 0.50
    
    # 4. Target Sensitivity >= 70%
    mask_70 = r >= 0.70
    t_sens70 = t[mask_70][np.argmax(p[mask_70])] if np.any(mask_70) else 0.50
    
    # 5. Raw Max PPV (with min sens 1%)
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
    print_flush("=" * 80)
    print_flush("      RANDOM FOREST THRESHOLD OPTIMIZATION FOR DAISY PROJECT")
    print_flush("=" * 80)
    
    # 1. Load Model
    model_path = find_rf_model()
    print_flush(f"\n[1/5] Loading Random Forest model from:\n      {model_path}")
    rf_model = load(model_path)
    if hasattr(rf_model, 'n_jobs'):
        rf_model.n_jobs = -1
    print_flush(f"      Model type: {type(rf_model).__name__}")
    
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
    
    # 3. Model Inference & Discrimination Metrics (AUROC, AUPRC)
    print_flush("\n[3/5] Computing predicted probabilities and discrimination metrics...")
    y_train_proba = rf_model.predict_proba(X_train)[:, 1]
    y_test_proba  = rf_model.predict_proba(X_test)[:, 1]
    y_gw_proba    = rf_model.predict_proba(X_gw)[:, 1]
    
    discrim_summary = pd.DataFrame([
        {"Dataset": "Leipzig Train", "Samples": len(y_train), "Positives": y_train.sum(), "AUROC": roc_auc_score(y_train, y_train_proba), "AUPRC": average_precision_score(y_train, y_train_proba)},
        {"Dataset": "Leipzig Validation (Test)", "Samples": len(y_test), "Positives": y_test.sum(), "AUROC": roc_auc_score(y_test, y_test_proba), "AUPRC": average_precision_score(y_test, y_test_proba)},
        {"Dataset": "Greifswald (External Test)", "Samples": len(y_gw), "Positives": y_gw.sum(), "AUROC": roc_auc_score(y_gw, y_gw_proba), "AUPRC": average_precision_score(y_gw, y_gw_proba)},
    ])
    
    print_flush("\n" + "-" * 80)
    print_flush("DISCRIMINATION METRICS (AUROC & AUPRC):")
    print_flush("-" * 80)
    print_flush(discrim_summary.to_string(index=False))
    
    # 4. Precision-Recall Curve Optimization
    print_flush("\n[4/5] Optimizing thresholds on PR Curve (TRAIN dataset)...")
    strategies, thresh_df = optimize_pr_curve(y_train, y_train_proba)
    
    # Evaluate across all datasets
    def evaluate_strategies(dataset_name, X_data, y_data, y_proba):
        rows = []
        for strat_name, thresh in strategies.items():
            y_pred = (y_proba >= thresh).astype(int)
            m = calculate_metrics(y_data, y_pred, y_proba)
            rows.append({
                "Strategy": strat_name,
                "Threshold": thresh,
                "PPV (%)": m["PPV (Precision)"] * 100,
                "Sensitivity (%)": m["Sensitivity (Recall)"] * 100,
                "Specificity (%)": m["Specificity"] * 100,
                "F1-Score": m["F1-Score"],
                "TP": m["TP"],
                "FP": m["FP"],
                "AUROC": m["AUROC"],
                "AUPRC": m["AUPRC"]
            })
        return pd.DataFrame(rows)

    train_eval = evaluate_strategies("Leipzig Train", X_train, y_train, y_train_proba)
    test_eval  = evaluate_strategies("Leipzig Test", X_test, y_test, y_test_proba)
    gw_eval    = evaluate_strategies("Greifswald Ext", X_gw, y_gw, y_gw_proba)
    
    print_flush("\n" + "-" * 80)
    print_flush("TRAIN DATASET THRESHOLD EVALUATION:")
    print_flush("-" * 80)
    print_flush(train_eval[["Strategy", "Threshold", "PPV (%)", "Sensitivity (%)", "Specificity (%)", "F1-Score", "TP", "FP"]].to_string(index=False))

    print_flush("\n" + "-" * 80)
    print_flush("INTERNAL TEST DATASET EVALUATION (LEIPZIG VALIDATION):")
    print_flush("-" * 80)
    print_flush(test_eval[["Strategy", "Threshold", "PPV (%)", "Sensitivity (%)", "Specificity (%)", "F1-Score", "TP", "FP"]].to_string(index=False))

    print_flush("\n" + "-" * 80)
    print_flush("EXTERNAL TEST DATASET EVALUATION (GREIFSVALD VALIDATION):")
    print_flush("-" * 80)
    print_flush(gw_eval[["Strategy", "Threshold", "PPV (%)", "Sensitivity (%)", "Specificity (%)", "F1-Score", "TP", "FP"]].to_string(index=False))

    # 5. Diagnostic Visualization Plot
    print_flush("\n[5/5] Generating diagnostic multi-panel visualization plot...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Subplot 1: PR Curves across datasets
    for d_name, yt, yp, color in [("Leipzig Train", y_train, y_train_proba, "navy"), ("Leipzig Test", y_test, y_test_proba, "teal"), ("Greifswald Ext", y_gw, y_gw_proba, "darkred")]:
        pr_p, pr_r, _ = precision_recall_curve(yt, yp)
        auprc_val = average_precision_score(yt, yp)
        axes[0, 0].plot(pr_r, pr_p, color=color, lw=2, label=f"{d_name} (AUPRC={auprc_val:.4f})")
    axes[0, 0].set_title("Precision-Recall Curves")
    axes[0, 0].set_xlabel("Recall (Sensitivity)")
    axes[0, 0].set_ylabel("Precision (PPV)")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: ROC Curves across datasets
    from sklearn.metrics import roc_curve
    for d_name, yt, yp, color in [("Leipzig Train", y_train, y_train_proba, "navy"), ("Leipzig Test", y_test, y_test_proba, "teal"), ("Greifswald Ext", y_gw, y_gw_proba, "darkred")]:
        fpr, tpr, _ = roc_curve(yt, yp)
        auroc_val = roc_auc_score(yt, yp)
        axes[0, 1].plot(fpr, tpr, color=color, lw=2, label=f"{d_name} (AUROC={auroc_val:.4f})")
    axes[0, 1].plot([0, 1], [0, 1], 'k--', alpha=0.5)
    axes[0, 1].set_title("Receiver Operating Characteristic (ROC) Curves")
    axes[0, 1].set_xlabel("False Positive Rate (1 - Specificity)")
    axes[0, 1].set_ylabel("True Positive Rate (Sensitivity)")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Subplot 3: PPV & Sensitivity vs Threshold (Train)
    axes[0, 2].plot(thresh_df["Threshold"], thresh_df["PPV"], label="PPV (Precision)", color="navy", lw=2)
    axes[0, 2].plot(thresh_df["Threshold"], thresh_df["Recall"], label="Sensitivity", color="darkorange", lw=2)
    axes[0, 2].axvline(strategies["PR Max F2 (Clinical Safety)"], color="green", linestyle="--", label=f"F2 Opt ({strategies['PR Max F2 (Clinical Safety)']:.4f})")
    axes[0, 2].set_title("PPV & Sensitivity vs Threshold (Train)")
    axes[0, 2].set_xlabel("Threshold")
    axes[0, 2].set_ylabel("Score")
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)

    # Subplot 4: F1 & F2 Scores vs Threshold (Train)
    axes[1, 0].plot(thresh_df["Threshold"], thresh_df["F1"], label="F1-Score (Balanced)", color="purple", lw=2)
    axes[1, 0].plot(thresh_df["Threshold"], thresh_df["F2"], label="F2-Score (Safety Weighted)", color="darkgreen", lw=2)
    axes[1, 0].axvline(strategies["PR Max F2 (Clinical Safety)"], color="green", linestyle="--", label=f"F2 Thresh ({strategies['PR Max F2 (Clinical Safety)']:.4f})")
    axes[1, 0].set_title("F1 & F2 Tradeoff vs Threshold (Train)")
    axes[1, 0].set_xlabel("Threshold")
    axes[1, 0].set_ylabel("Score")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Subplot 5: Internal Test Confusion Matrix @ Recommended F2 Threshold
    f2_thresh = strategies["PR Max F2 (Clinical Safety)"]
    cm_test = confusion_matrix(y_test, (y_test_proba >= f2_thresh).astype(int))
    disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=["Control", "Sepsis"])
    disp_test.plot(ax=axes[1, 1], cmap="Blues", values_format="d")
    axes[1, 1].set_title(f"Leipzig Test CM @ F2 Thresh ({f2_thresh:.4f})")

    # Subplot 6: External Test Confusion Matrix @ Recommended F2 Threshold
    cm_gw = confusion_matrix(y_gw, (y_gw_proba >= f2_thresh).astype(int))
    disp_gw = ConfusionMatrixDisplay(confusion_matrix=cm_gw, display_labels=["Control", "Sepsis"])
    disp_gw.plot(ax=axes[1, 2], cmap="Oranges", values_format="d")
    axes[1, 2].set_title(f"Greifswald Ext CM @ F2 Thresh ({f2_thresh:.4f})")

    plt.tight_layout()
    plot_out = os.path.join(SCRIPT_DIR, "rf_ppv_threshold_analysis.png")
    plt.savefig(plot_out, dpi=300)
    print_flush(f"      Diagnostic plot saved to: {plot_out}")
    
    print_flush("\n" + "=" * 80)
    print_flush("OPTIMIZATION COMPLETE!")
    print_flush("=" * 80)


if __name__ == "__main__":
    main()
