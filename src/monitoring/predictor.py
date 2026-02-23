# src/monitoring/predictor.py
import joblib
from tensorflow.keras.models import load_model
from src.config import settings
import numpy as np

# Load trained models
rf_model = joblib.load(settings.RF_MODEL_PATH)
lstm_model = load_model(settings.LSTM_MODEL_PATH)
scaler = joblib.load(settings.SCALER_PATH)

def predict_anomaly(metrics):
    """
    Predict anomaly based on system metrics using RF & LSTM
    """
    # Example: RF expects scaled input
    input_scaled = scaler.transform([[metrics['cpu'], metrics['ram'], metrics['disk']]])
    rf_pred = rf_model.predict(input_scaled)[0]

    # LSTM expects 3D input (1, timesteps, features)
    lstm_input = np.array([[metrics['cpu'], metrics['ram'], metrics['disk']]]).reshape((1,1,3))
    lstm_pred = lstm_model.predict(lstm_input)[0][0]

    # Simple ensemble logic: if either predicts anomaly, flag
    anomaly = rf_pred == 1 or lstm_pred > 0.5
    return anomaly