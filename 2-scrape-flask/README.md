# Complete Guide: Scraping Flask Metrics in Kubernetes

This guide explains how to connect a Flask application to the **kube-prometheus-stack** using a **ServiceMonitor**.

## 1. Start Minikube and Install Prometheus

- **Start Minikube** (example with 3 nodes):
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

## 2. Deploy the Example App

The app is a Flask service that exposes a `/metrics` endpoint. The Kubernetes setup consists of three resources:

- **Deployment** (`app-deployment.yaml`) — deploys the pods; `containerPort` must match the Python code
- **Service** (`app-service.yaml`) — must have a named port so the ServiceMonitor can identify it
- **ServiceMonitor** (`flask-monitor.yaml`) — tells Prometheus to scrape the Service

Build the Docker image, push it, and apply all resources in one step:
```
bash deploy-app.sh
```

> **Note:** `deploy-app.sh` pushes to a Docker Hub registry. Update the image name in the script to point to your own repository before running.

### Custom Metrics

The app exposes three custom metrics on top of the automatic Flask defaults:

| Metric | Type | Description |
|--------|------|-------------|
| `shop_orders_total` | Counter | Orders placed, labelled by `category` (electronics / clothing / food) |
| `shop_active_users` | Gauge | Users currently logged in |
| `shop_payment_duration_seconds` | Histogram | Simulated payment processing time in seconds |

### Routes

| Route | What it does |
|-------|-------------|
| `GET /` | Health-check / welcome message |
| `GET /buy/<category>` | Places an order, records payment duration |
| `GET /login` | Increments active-user count |
| `GET /logout` | Decrements active-user count |

## 3. Try with Prometheus

**Access the Prometheus UI:**
```
kubectl port-forward svc/kube-stack-kube-prometheus-prometheus -n monitoring 9090:9090
```
Open `http://localhost:9090`. Go to **Status -> Target Health** and confirm `flask-app-monitor` shows **UP**.

**Generate some traffic:**
```bash
# Replace <HOST> with the minikube service URL or localhost if port-forwarding
curl http://<HOST>/buy/electronics
curl http://<HOST>/buy/food
curl http://<HOST>/login
curl http://<HOST>/logout
```

**Built-in Flask metrics:**
* `flask_http_request_total` — raw request counts per pod
* `sum(flask_http_request_total) by (status)` — aggregated by HTTP status code
* `rate(flask_http_request_total[1m])` — requests per second

**Custom shop metrics:**
* `shop_orders_total` — total orders placed
* `sum(shop_orders_total) by (category)` — orders broken down by product category
* `rate(shop_orders_total[1m])` — order rate per second
* `shop_active_users` — currently logged-in users (live gauge)
* `histogram_quantile(0.95, rate(shop_payment_duration_seconds_bucket[5m]))` — 95th-percentile payment processing time

## 4. Try with Grafana

**Access Grafana:**
```
kubectl port-forward svc/kube-stack-grafana 3000:80 -n monitoring
```
Browse to `http://localhost:3000`. Get the admin password with:
```
kubectl get secret -n monitoring kube-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

---

### Option A — Build a Dashboard Manually

1. Click **+** (top-right) → **New dashboard** → **Add visualization**
2. Select **Prometheus** as the data source
3. In the **Metrics** field enter a query (see examples below) and click **Run query**
4. Set a panel title, then click **Apply**
5. Repeat for each panel, then click the **Save** icon (top-right) and give the dashboard a name

Suggested panels:

| Panel title | Query |
|-------------|-------|
| Order Rate by Category | `sum(rate(shop_orders_total[1m])) by (category)` |
| Active Users | `shop_active_users` |
| Payment Duration p95 | `histogram_quantile(0.95, rate(shop_payment_duration_seconds_bucket[5m]))` |
| HTTP Request Rate | `sum(rate(flask_http_request_total[1m])) by (status)` |

---

### Option B — Import the Ready-Made Dashboard

A pre-built dashboard with all four panels is provided in `flask-dashboard.json`.

1. In Grafana click **+** → **Import dashboard**
2. Click **Upload JSON file** and select `flask-dashboard.json`
3. Select **Prometheus** as the data source and click **Import**

The dashboard auto-refreshes every 10 seconds and shows the last 15 minutes of data.
