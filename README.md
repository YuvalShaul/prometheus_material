## How to run

You can run prometheus using docker, like this:
```
docker run -d  \
 --name prometheus \
 --network host  \
 -v /home/osboxes/Documents/prometheus_material/prometheus.yml:/etc/prometheus/prometheus.yml \  prom/prometheus
```
It means:
- run a container called **prometheus**
- We'll be using the host network, so we can connect to the node_exporter (that we'll run next)
- map the directory you created **prometheus.yml** configuration file to the /etc/prometheus directory **inside the container**
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