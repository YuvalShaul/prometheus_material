#!/bin/bash
#
# This script builds the Docker image for the Flask application.
# The image name (flask-app) matches my private docker hub registry.
# You should creatae your own repository on Docker Hub 
#   and change the image name in the docker build and push commands below.

docker build -t yuvalshaul/flask-app .
docker push yuvalshaul/flask-app

kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml
minikube -p four tunnel

