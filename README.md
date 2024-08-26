## How to run

You can run prometheus using docker, like this:
```
docker run -d  \
 --name prometheus \
 -p 9090:9090  \
 -v /home/osboxes/Documents/prometheus_material/prometheus.yml:/etc/prometheus/prometheus.yml \  prom/prometheus
```
It means:
- run a container called **prometheus**
- connect port 9090 of this container to the running node 9090 port
- map the directory you created **prometheus.yml** configuration file to the /etc/prometheus directory **inside the container**
- use this image:  prom/prometheus (from dockerhub)

If everything is OK, you can brose to localhost:9090

