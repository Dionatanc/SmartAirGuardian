# backend/app/ml/models_loader.py

import os
from typing import Dict, Any

import numpy as np
import joblib


class MLModels:
    def __init__(self, models_dir: str = "backend/app/ml/data/models"):
        iso_path = os.path.join(models_dir, "isolation_forest.pkl")
        rf_path = os.path.join(models_dir, "random_forest_risk.pkl")
        lr_path = os.path.join(models_dir, "linear_regression_co2.pkl")

        if not (os.path.exists(iso_path) and os.path.exists(rf_path) and os.path.exists(lr_path)):
            raise FileNotFoundError(
                "Modelos não encontrados. Rode backend/app/ml/train_models.py primeiro."
            )

        self.isolation_forest = joblib.load(iso_path)
        self.random_forest = joblib.load(rf_path)
        self.linear_regression = joblib.load(lr_path)

    def predict_all(self, co2: float, pm25: float, temp: float, humidity: float) -> Dict[str, Any]:
        """
        Recebe uma leitura de sensor e retorna:
        - anomaly (bool)
        - risk_level (int)
        - co2_next_pred (float)
        """
        X = np.array([[co2, pm25, temp, humidity]])

        # Isolation Forest: -1 anômalo, 1 normal
        anomaly_pred = int(self.isolation_forest.predict(X)[0])
        is_anomaly = anomaly_pred == -1

        # Risco
        risk_level = int(self.random_forest.predict(X)[0])

        # Previsão de CO2
        co2_next_pred = float(self.linear_regression.predict(X)[0])

        return {
            "is_anomaly": is_anomaly,
            "risk_level": risk_level,
            "co2_next_pred": co2_next_pred,
        }


# helper global (opcional)
ml_models: MLModels | None = None


def get_ml_models() -> MLModels:
    global ml_models
    if ml_models is None:
        ml_models = MLModels()
    return ml_models
