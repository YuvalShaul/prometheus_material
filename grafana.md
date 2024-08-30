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

Browse to Grafana on [localhost:3000](localhost:3000)   
Use admin/admin as user and password.

## Connect to Prometheus

- On the grafana **home** page (you can use the menu to get there) locate the **DATA SOURCES** cube and click it.
- Find and click **Promethus**
- Name your new data source (I called mine **local-prometheus**)
- Fill in the url.  
Note that this field my look as if it already has the correct value, but it is really empty.  
I use the defauld for Prometheus:  
**http://localhost:9090**
- Go to **Authentication**, select **Basic authentication** and fill in the credentials (admin/admin in my case)
- Leave everything else as it is, and click **Save & test** at the bottom.  
You should get a seccessful resutl

## Create a new Dashboard

- Locate **Dashboards** on the menu, and click
- Click on **Create dashboard**


