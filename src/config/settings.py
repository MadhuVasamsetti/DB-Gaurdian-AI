# src/config/settings.py

# Monitoring configuration
MONITOR_INTERVAL = 5          # seconds between system checks
ALERT_THRESHOLD_CPU = 85      # % CPU usage to trigger alert
ALERT_THRESHOLD_RAM = 90      # % RAM usage to trigger alert
ALERT_THRESHOLD_DISK = 90     # % Disk usage to trigger alert

# File paths
DATASET_PATH = "data/database_metrics.csv"
RF_MODEL_PATH = "models/rf_model.pkl"
LSTM_MODEL_PATH = "models/lstm_model.h5"
SCALER_PATH = "models/scaler.pkl"
LOG_FILE = "logs/monitoring.log"