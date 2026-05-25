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

* `flask_http_request_total`: Shows raw request counts per pod.
* `sum(flask_http_request_total) by (status)`: Aggregates requests by success/error code.
* `rate(flask_http_request_total[1m])`: Shows current traffic "speed" (requests per second).
