"""
train_models.py

Trains ML models (Random Forest, XGBoost) and an LSTM on the engineered
features, to compare against the classical baselines in train_baselines.py.

Output: models/rf_model.pkl, models/xgb_model.pkl, models/lstm_model.pt
"""

import pandas as pd
# TODO: from sklearn.ensemble import RandomForestRegressor
# TODO: import xgboost as xgb
# TODO: import torch, torch.nn as nn  (for LSTM)

RANDOM_SEED = 42  # fix for reproducibility


def train_random_forest(X_train, y_train):
    raise NotImplementedError


def train_xgboost(X_train, y_train):
    raise NotImplementedError


def train_lstm(X_train, y_train, epochs: int = 50):
    raise NotImplementedError


if __name__ == "__main__":
    df = pd.read_csv("data/features.csv", parse_dates=["date"])
    # TODO: chronological split, then train each model
