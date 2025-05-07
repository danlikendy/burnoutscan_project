
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np
import os

# Определяем путь к модели относительно текущего файла

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "rf_balanced_model.pkl")

# Загружаем модель

model = joblib.load(model_path)

# Список признаков

FEATURES = [
    "avg_sent", "median_sent", "max_sent", "std_sent",
    "active_days_x", "night_ratio", "weekend_ratio",
    "avg_msgs_per_day", "unique_recipients"
]

# Входные данные

class InputFeatures(BaseModel):
    avg_sent: float
    median_sent: float
    max_sent: float
    std_sent: float
    active_days_x: int
    night_ratio: float
    weekend_ratio: float
    avg_msgs_per_day: float
    unique_recipients: int

# Инициализация приложения

app = FastAPI()

# Одиночный прогноз

@app.post("/predict")
def predict_risk(data: InputFeatures):
    X = np.array([[getattr(data, feat) for feat in FEATURES]])
    prob = model.predict_proba(X)[0][1]
    label = "риск" if prob > 0.5 else "норма"
    return {
        "prediction": label,
        "probability": round(float(prob), 3)
    }

# Массовый прогноз

@app.post("/bulk_predict")
def bulk_predict(data: List[InputFeatures]):
    X = np.array([[getattr(row, feat) for feat in FEATURES] for row in data])
    probs = model.predict_proba(X)[:, 1]
    results = []
    for prob in probs:
        label = "риск" if prob > 0.5 else "норма"
        results.append({
            "prediction": label,
            "probability": round(float(prob), 3)
        })
    return results
