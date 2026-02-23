# src/monitoring/system_metrics.py
import psutil

def get_system_metrics():
    """
    Returns live system metrics: CPU, RAM, Disk usage
    """
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return {"cpu": cpu, "ram": ram, "disk": disk}