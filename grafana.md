## Run Grafana

Here's how you can run [Grafana](https://grafana.com/) on docker:  
```
docker run \
  -d \
  -p 3000:3000 \
  --name=grafana \
  --network host \
  grafana/grafana-enterprise
```

