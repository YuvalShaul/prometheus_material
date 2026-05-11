## Install Prometheus using Helm

Assunimg you have [Helm](https://helm.sh/) already installed:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```


kubectl create namespace monitoring
helm install kube-stack prometheus-community/kube-prometheus-stack --namespace monitoring





===============================================================================

kubectl port-forward svc/kube-stack-grafana  3000:80 -n monitoring 



http://localhost:3000

Username: admin

kubectl get secret -n monitoring kube-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
Password: 
