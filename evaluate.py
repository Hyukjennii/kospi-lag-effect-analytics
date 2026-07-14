"""
evaluate.py

Walk-forward (rolling-origin) validation of all models, followed by a
Diebold-Mariano test to check whether any ML model's improvement over the
best baseline is statistically significant - not just numerically higher.
Finishes with SHAP interpretation of the best model.

Output: results/model_comparison.csv, results/dm_test_results.csv,
        docs/diagrams/shap_summary.png
"""

import pandas as pd
# TODO: import shap
# TODO: from dieboldmariano import dm_test  (or implement manually)


def walk_forward_validate(model_fn, df: pd.DataFrame, initial_train_size: int, step: int = 1):
    """
    Rolling-origin validation: train on [0:t], predict t+1, then expand the
    window and repeat. Never use k-fold on time series data.
    """
    raise NotImplementedError


def compute_metrics(y_true, y_pred) -> dict:
    """RMSE, MAE, and directional accuracy (did we predict up/down correctly)."""
    raise NotImplementedError


def run_diebold_mariano(errors_baseline, errors_model) -> dict:
    """Tests whether errors_model is significantly more accurate than errors_baseline."""
    raise NotImplementedError


def run_shap(model, X):
    """SHAP feature attribution for the best-performing model."""
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: load predictions from all models, run walk-forward validation,
    # compute metrics, run DM test against best baseline, run SHAP, save results
    pass
