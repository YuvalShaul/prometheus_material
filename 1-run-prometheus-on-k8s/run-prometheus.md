### Install Prometheus using Helm

- Assunimg you have [Helm](https://helm.sh/) already installed:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
- Assuming **kubectl** is installed and points to a k8s cluster:
  - Create a namespace for all Prometheus components:
  ```
  kubectl create namespace monitoring
  ```
  - Install Prometheus:
  ```
  helm install kube-stack prometheus-community/kube-prometheus-stack --namespace monitoring
  ```


### Exposing Grafana using port-forward command
- Using the [port-forward](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/) command:
```
kubectl port-forward svc/kube-stack-grafana  3000:80 -n monitoring 
```
- Browse grafana:
  - user name:
  http://localhost:3000
  - Get password using this command:
  ```
  kubectl get secret -n monitoring kube-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
  ```
