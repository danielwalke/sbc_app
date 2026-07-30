#!/usr/bin/env python3
"""
Test & Verification Suite for XGBoost Thresholds (Max F2 vs. Max G-Mean)

This script:
1. Loads the standard XGBoost classifier.
2. Preprocesses SBC dataset into Leipzig Train, Leipzig Validation (Test), and Greifswald External Validation.
3. Computes the optimal Max G-Mean (ROC-based) and Max F2 (PR-based) thresholds on Leipzig Train.
4. Evaluates both thresholds across all three datasets and computes exact Confusion Matrices and metrics.
5. Runs assertion tests to verify exact match with expected benchmark metrics.
"""

import os
import sys
import zipfile
import unittest
import numpy as np
import pandas as pd
from joblib import load
from sklearn.metrics import (
    roc_curve,
    precision_recall_curve,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)

# Ensure path resolution
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


def load_xgb_model():
    """Load standard XGBoost model."""
    xgb_paths = [
        os.path.join(BACKEND_DIR, "models", "standard", "xgb.joblib"),
        os.path.join(SCRIPT_DIR, "models", "standard", "xgb.joblib")
    ]
    for p in xgb_paths:
        if os.path.isfile(p):
            return load(p)
    raise FileNotFoundError("Could not locate models/standard/xgb.joblib.")


def evaluate_threshold(y_true, y_proba, threshold):
    """Compute detailed confusion matrix and metrics at a given threshold."""
    y_pred = (y_proba >= threshold).astype(int)
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    sensitivity = recall_score(y_true, y_pred, zero_division=0)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    ppv = precision_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    return {
        "Threshold": threshold,
        "Confusion_Matrix": cm,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp,
        "Sensitivity": sensitivity,
        "Specificity": specificity,
        "PPV": ppv,
        "F1": f1
    }


def run_threshold_evaluations():
    """Execute complete threshold optimization and evaluation pipeline."""
    print_flush("=" * 80)
    print_flush("      XGBOOST THRESHOLD VERIFICATION SUITE (MAX F2 vs MAX G-MEAN)")
    print_flush("=" * 80)
    
    # 1. Load Model & Data
    xgb = load_xgb_model()
    dataset_path = find_sbc_dataset()
    df_raw = pd.read_csv(dataset_path)
    
    da = DataAnalysis(data=df_raw, print_logs=False)
    X_train, y_train = da.get_X_train(), da.get_y_train()
    X_test, y_test   = da.get_X_test(), da.get_y_test()
    X_gw, y_gw       = da.get_X_gw(), da.get_y_gw()
    
    # 2. Compute Probabilities
    y_train_p = xgb.predict_proba(X_train)[:, 1]
    y_test_p  = xgb.predict_proba(X_test)[:, 1]
    y_gw_p    = xgb.predict_proba(X_gw)[:, 1]
    
    # 3. Optimize Thresholds on Leipzig Train Set
    # A. Max G-Mean (ROC Curve)
    fpr, tpr, roc_thresholds = roc_curve(y_train, y_train_p)
    spec = 1 - fpr
    g_means = np.sqrt(tpr * spec)
    t_gmean = roc_thresholds[np.argmax(g_means)]
    
    # B. Max F2 Score (PR Curve)
    pr_p, pr_r, pr_t = precision_recall_curve(y_train, y_train_p)
    p, r, t = pr_p[:-1], pr_r[:-1], pr_t
    f2_scores = np.where((4 * p + r) > 0, 5 * (p * r) / (4 * p + r), 0)
    t_f2 = t[np.argmax(f2_scores)]
    
    print_flush(f"\n[Calculated Thresholds on Leipzig Train]")
    print_flush(f"  • Max G-Mean Threshold (ROC-based): {t_gmean:.6f}")
    print_flush(f"  • Max F2 Threshold (PR-based):      {t_f2:.6f}")
    
    # 4. Evaluate Thresholds across Cohorts
    results = {
        "Max_GMean": {
            "Threshold": t_gmean,
            "Train": evaluate_threshold(y_train, y_train_p, t_gmean),
            "Test":  evaluate_threshold(y_test, y_test_p, t_gmean),
            "GW":    evaluate_threshold(y_gw, y_gw_p, t_gmean)
        },
        "Max_F2": {
            "Threshold": t_f2,
            "Train": evaluate_threshold(y_train, y_train_p, t_f2),
            "Test":  evaluate_threshold(y_test, y_test_p, t_f2),
            "GW":    evaluate_threshold(y_gw, y_gw_p, t_f2)
        }
    }
    
    # 5. Display Formatted Confusion Matrices & Metrics
    print_flush("\n" + "=" * 80)
    print_flush("CONFUSION MATRICES & EVALUATION METRICS:")
    print_flush("=" * 80)
    
    for strat_name, strat_data in results.items():
        tr = strat_data["Threshold"]
        print_flush(f"\n>>> STRATEGY: {strat_name} (Threshold = {tr:.6f})")
        print_flush("-" * 65)
        for split_name, res in [("Leipzig Train", strat_data["Train"]), ("Leipzig Validation (Test)", strat_data["Test"]), ("Greifswald External", strat_data["GW"])]:
            cm = res["Confusion_Matrix"]
            print_flush(f"\n  Cohort: {split_name}")
            print_flush(f"    Confusion Matrix [[TN, FP], [FN, TP]]:")
            print_flush(f"      [[{cm[0,0]:7d}, {cm[0,1]:7d}],")
            print_flush(f"       [{cm[1,0]:7d}, {cm[1,1]:7d}]]")
            print_flush(f"    Sensitivity (Recall): {res['Sensitivity']*100:6.2f}%")
            print_flush(f"    Specificity:          {res['Specificity']*100:6.2f}%")
            print_flush(f"    PPV (Precision):      {res['PPV']*100:6.2f}%")
            print_flush(f"    F1-Score:             {res['F1']:.4f}")
            
    # 6. Run Automated Verification Tests
    print_flush("\n" + "=" * 80)
    print_flush("RUNNING AUTOMATED VERIFICATION ASSERTIONS...")
    print_flush("=" * 80)
    
    # Expected Benchmark Metrics for Validation
    # Max G-Mean Greifswald Sens ~75.00%, Spec ~70.50%
    # Max F2 Greifswald Sens ~19.87%, Spec ~97.44%
    assert np.isclose(results["Max_GMean"]["GW"]["Sensitivity"], 0.7500, atol=0.01), "G-Mean Greifswald Sensitivity Mismatch!"
    assert np.isclose(results["Max_GMean"]["GW"]["Specificity"], 0.7050, atol=0.01), "G-Mean Greifswald Specificity Mismatch!"
    assert np.isclose(results["Max_F2"]["GW"]["Sensitivity"], 0.1987, atol=0.01), "Max F2 Greifswald Sensitivity Mismatch!"
    assert np.isclose(results["Max_F2"]["GW"]["Specificity"], 0.9744, atol=0.01), "Max F2 Greifswald Specificity Mismatch!"
    
    print_flush("\n✅ ALL ASSERTION TESTS PASSED SUCCESSFULLY! Empirical metrics match benchmark values.")
    print_flush("=" * 80)
    
    return results


if __name__ == "__main__":
    run_threshold_evaluations()
