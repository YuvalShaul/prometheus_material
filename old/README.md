## How to run
- Assuming you have cloned this git repository:  
  - Prometheus needs a config file (prometheus.yml from this directory)
  - You can run prometheus using docker, like this:  
(remember to change the directory name)
```
docker run -d  \
 --name prometheus \
 --network host  \
 -v /home/yuval/Documents/prometheus_material/prometheus.yml:/etc/prometheus/prometheus.yml  \
 prom/prometheus
```
- It means:
  - run a container called **prometheus**
  - We'll be using the host network, so we can connect to the node_exporter (that we'll run next)
  - map the prometheus config file to the one on the host: **prometheus.yml*
- use this image:  prom/prometheus (from dockerhub)

If everything is OK, you can brose to localhost:9090

## Making sure you cam monitor your own host

You should run a [node_exporter](https://prometheus.io/docs/guides/node-exporter/), the component that will be available for Prometheus scraping.  
You can do this using docker:

```
docker run -d \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```


## Try out quesries

Try the following queries:
- node_cpu_seconds_total
- node_cpu_seconds_total{mode="idle"}
- node_cpu_seconds_total{mode="idle", cpu="1"}
- node_cpu_seconds_total{mode="idle", cpu="1"}[2m]
- rate(node_cpu_seconds_total{mode="idle", cpu="1"}[2m])
- rate(node_cpu_seconds_total{mode="idle"}[2m])
- avg(rate(node_cpu_seconds_total{mode="idle"}[2m]))
