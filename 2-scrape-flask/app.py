from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

# 1. It creates the /metrics endpoint
# 2. It "Wraps" your functions (The Middleware)
#    It records if the page was a success (200 OK) or an error (500 Error).
# 3. It tracks the "Default Four"
#    Without you writing a single extra line of code, importing and initializing this library starts tracking:
#       Request Count: How many people visited?
#       Request Latency: How slow is the app?
#       In-progress Requests: How many people are hitting the server right now?
#       HTTP Status Codes: How many 404s or 500s are happening?



app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
