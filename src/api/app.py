import sys
import os
from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, session, url_for

# Fix import path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from src.monitoring.system_metrics import get_system_metrics
from src.monitoring.predictor import predict_anomaly



app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "supersecretkey123"



ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", active="dashboard")



@app.route("/metrics")
@login_required
def metrics():
    return render_template("metrics.html", active="metrics")



@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", active="settings")



@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", active="profile")



@app.route("/live-data")
@login_required
def live_data():
    raw_metrics = get_system_metrics()
    metrics = {
        "cpu": float(raw_metrics.get("cpu", 0)),
        "ram": float(raw_metrics.get("ram", 0)),
        "disk": float(raw_metrics.get("disk", 0))
    }
    anomaly = bool(predict_anomaly(metrics))

    health_score = 100
    if anomaly:
        health_score -= 20
    if metrics["cpu"] > 85:
        health_score -= 10
    if metrics["ram"] > 90:
        health_score -= 10
    if metrics["disk"] > 90:
        health_score -= 10
    health_score = max(health_score, 0)

    return jsonify({
        "metrics": metrics,
        "anomaly": anomaly,
        "health_score": health_score
    })



if __name__ == "__main__":
    print("🚀 DB Guardian AI Running...")
    print("Login at: http://127.0.0.1:5000/login")
    app.run(debug=True)