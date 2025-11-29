# backend/app/ml/train_models.py

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib


def generate_synthetic_data(n_samples: int = 2000) -> pd.DataFrame:
    """
    Gera um dataset sintético de qualidade do ar.
    Colunas: co2, pm25, temp, humidity, risk_level, next_co2.
    """
    rng = np.random.default_rng(42)

    co2 = rng.normal(loc=450, scale=80, size=n_samples)      # ppm
    pm25 = rng.normal(loc=25, scale=10, size=n_samples)      # µg/m3
    temp = rng.normal(loc=24, scale=3, size=n_samples)       # °C
    humidity = rng.normal(loc=55, scale=10, size=n_samples)  # %

    # normaliza faixas
    co2 = np.clip(co2, 300, 1000)
    pm25 = np.clip(pm25, 5, 120)
    temp = np.clip(temp, 15, 35)
    humidity = np.clip(humidity, 20, 90)

    # regra simples para risco (0 baixo, 1 moderado, 2 alto, 3 perigoso)
    risk_level = []
    for c, pm in zip(co2, pm25):
        if c < 500 and pm < 25:
            risk_level.append(0)
        elif c < 700 and pm < 40:
            risk_level.append(1)
        elif c < 900 and pm < 70:
            risk_level.append(2)
        else:
            risk_level.append(3)

    risk_level = np.array(risk_level)

    # próxima leitura de CO2 (next_co2): usa tendência + ruído
    next_co2 = co2 + rng.normal(loc=0, scale=20, size=n_samples)
    next_co2 = np.clip(next_co2, 300, 1100)

    df = pd.DataFrame(
        {
            "co2": co2,
            "pm25": pm25,
            "temp": temp,
            "humidity": humidity,
            "risk_level": risk_level,
            "next_co2": next_co2,
        }
    )
    return df


def train_and_save_models():
    df = generate_synthetic_data()

    features = df[["co2", "pm25", "temp", "humidity"]]
    target_risk = df["risk_level"]
    target_next_co2 = df["next_co2"]

    # Isolation Forest (anomalias)
    iso_forest = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )
    iso_forest.fit(features)

    # Random Forest (classificação de risco)
    X_train, X_test, y_train, y_test = train_test_split(
        features, target_risk, test_size=0.2, random_state=42
    )
    rf_clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42,
    )
    rf_clf.fit(X_train, y_train)
    accuracy = rf_clf.score(X_test, y_test)
    print(f"Acurácia RandomForest (risco): {accuracy:.3f}")

    # Regressão Linear (previsão do próximo CO2)
    lr = LinearRegression()
    lr.fit(features, target_next_co2)
    r2 = lr.score(features, target_next_co2)
    print(f"R² Regressão Linear (next_co2): {r2:.3f}")

    # salvar modelos
    models_dir = os.path.join("data", "models")
    os.makedirs(models_dir, exist_ok=True)

    joblib.dump(iso_forest, os.path.join(models_dir, "isolation_forest.pkl"))
    joblib.dump(rf_clf, os.path.join(models_dir, "random_forest_risk.pkl"))
    joblib.dump(lr, os.path.join(models_dir, "linear_regression_co2.pkl"))

    print(f"Modelos salvos em: {models_dir}")


if __name__ == "__main__":
    train_and_save_models()
