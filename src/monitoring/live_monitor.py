# src/monitoring/live_monitor.py
import time
from src.monitoring.system_metrics import get_system_metrics
from src.monitoring.predictor import predict_anomaly
from src.monitoring.alert_system import send_alert
from src.config import settings
from src.utils import logger

def start_monitoring():
    print("🚀 Starting live system monitoring...")
    while True:
        metrics = get_system_metrics()
        logger.log_info(f"Metrics: {metrics}")

        # Check thresholds
        if (metrics['cpu'] > settings.ALERT_THRESHOLD_CPU or
            metrics['ram'] > settings.ALERT_THRESHOLD_RAM or
            metrics['disk'] > settings.ALERT_THRESHOLD_DISK):
            send_alert(metrics)

        # Check ML prediction
        if predict_anomaly(metrics):
            send_alert(metrics)

        time.sleep(settings.MONITOR_INTERVAL)

if __name__ == "__main__":
    start_monitoring()