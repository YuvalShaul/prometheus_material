# Complete Guide: Scraping Flask Metrics in Kubernetes

This guide explains how to connect a Flask application to the **kube-prometheus-stack** using a **ServiceMonitor**.

## 0. Prerequisites: Start Minikube and Install Prometheus

- **Start Minikube:**
An example with 3 nodes:
```
minikube start -p three -n 3
```

- **Install the kube-prometheus-stack Helm chart:**
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install kube-stack prometheus-community/kube-prometheus-stack --namespace monitoring
```

- **Access Grafana (optional):**
```
kubectl port-forward svc/kube-stack-grafana 3000:80 -n monitoring
```
Browse to `http://localhost:3000`. Get the admin password with:
```
kubectl get secret -n monitoring kube-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

## 1. The Application (Python)

- Your Flask app must use the `prometheus-flask-exporter` library to expose a `/metrics` route.
- All required libraries are already in **requirements.txt**

### Custom Metrics in `app.py`

The app defines three custom Prometheus metrics on top of the automatic defaults:

| Metric | Type | Description |
|--------|------|-------------|
| `shop_orders_total` | Counter | Orders placed, labelled by `category` (electronics / clothing / food) |
| `shop_active_users` | Gauge | Users currently logged in (increments on `/login`, decrements on `/logout`) |
| `shop_payment_duration_seconds` | Histogram | Simulated payment processing time in seconds |

### Routes to generate data

| Route | What it does |
|-------|-------------|
| `GET /` | Health-check / welcome message |
| `GET /buy/<category>` | Places an order, records payment duration |
| `GET /login` | Increments active-user count |
| `GET /logout` | Decrements active-user count |

Example — generate some traffic after deploying:
```bash
# Replace <HOST> with the minikube service URL or localhost if port-forwarding
curl http://<HOST>/buy/electronics
curl http://<HOST>/buy/food
curl http://<HOST>/login
curl http://<HOST>/logout
```

## 2. The Kubernetes Configuration

The "Handshake" happens through three YAML files.

- A. The Deployment (`deployment.yaml`)
Deploys the pods. Ensure the `containerPort` matches your Python code.


- B. The Service (`service.yaml`)
The Service **must** have a named port so the monitor can identify it.

- C. The ServiceMonitor (`servicemonitor.yaml`)
This tells Prometheus to "scrape" the Service.


## 3. Deployment Steps

- **Apply your app resources:**
(see di-all.sh bash file)
- **Access Prometheus UI:**
```
kubectl port-forward svc/kube-stack-kube-prometheus-prometheus -n monitoring 9090:9090

```

- **Verify the Targets:**
Open `http://localhost:9090` in your browser. Go to **Status -> Target Health**. You should see `flask-app-monitor` with an **UP** status.

## 4. Querying Results

In the Prometheus search bar, run:

**Built-in Flask metrics (from `prometheus-flask-exporter`):**
* `flask_http_request_total` — raw request counts per pod
* `sum(flask_http_request_total) by (status)` — aggregated by HTTP status code
* `rate(flask_http_request_total[1m])` — requests per second (traffic speed)

**Custom shop metrics:**
* `shop_orders_total` — total orders placed
* `sum(shop_orders_total) by (category)` — orders broken down by product category
* `rate(shop_orders_total[1m])` — order rate per second
* `shop_active_users` — currently logged-in users (live gauge)
* `histogram_quantile(0.95, rate(shop_payment_duration_seconds_bucket[5m]))` — 95th-percentile payment processing time
