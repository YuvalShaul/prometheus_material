from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge, Histogram
import random
import time

# PrometheusMetrics automatically provides:
#   - /metrics endpoint
#   - request count, latency, in-progress requests, and HTTP status codes

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# --- Custom metrics ---

# Counter: total number of orders placed, broken down by product category
orders_total = Counter(
    "shop_orders_total",
    "Total number of orders placed",
    ["category"]  # label: electronics, clothing, food
)

# Gauge: number of users currently logged in (goes up and down)
active_users = Gauge(
    "shop_active_users",
    "Number of currently active (logged-in) users"
)

# Histogram: simulated payment processing duration in seconds
payment_duration = Histogram(
    "shop_payment_duration_seconds",
    "Time spent processing a payment",
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
)

# --- Routes ---

@app.route("/")
def hello():
    return "Hello, World! Try /buy/<category>, /login, /logout"

@app.route("/buy/<category>")
def buy(category):
    """Simulate placing an order. Increments the orders counter for the given category."""
    allowed = {"electronics", "clothing", "food"}
    if category not in allowed:
        return jsonify(error=f"Unknown category. Use one of: {allowed}"), 400

    orders_total.labels(category=category).inc()

    # Simulate variable payment processing time
    duration = random.uniform(0.05, 3.0)
    payment_duration.observe(duration)
    time.sleep(min(duration, 0.1))  # cap actual sleep so the demo stays snappy

    return jsonify(status="order placed", category=category, processing_seconds=round(duration, 3))

@app.route("/login")
def login():
    """Simulate a user logging in."""
    active_users.inc()
    return jsonify(status="logged in", active_users=active_users._value.get())

@app.route("/logout")
def logout():
    """Simulate a user logging out."""
    active_users.dec()
    return jsonify(status="logged out", active_users=active_users._value.get())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
