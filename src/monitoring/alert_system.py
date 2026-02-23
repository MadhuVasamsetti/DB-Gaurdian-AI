# src/monitoring/alert_system.py
from src.utils import logger

def send_alert(metrics):
    message = f"⚠️ ALERT! High system usage detected: CPU={metrics['cpu']}%, RAM={metrics['ram']}%, Disk={metrics['disk']}%"
    print(message)
    logger.log_warning(message)