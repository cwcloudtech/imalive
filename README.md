# Im Alive

👋 Welcome to Im Alive metrics exporter!

<p align="center">
    <img src="./img/logo.png"/>
</p>

Let your machines sing like Céline Dion `I'm alive!`.

<p align="center">
    <img src="./img/celine.jpeg"/>
</p>

Just a dummy healthcheck api and metric exporter for your nodes. It's also supported by [comwork cloud](https://doc.cloud.comwork.io/docs/tutorials/imalive).

It provide a http/restful endpoint that you can use as a healthcheck rule to your loadbalancer and also publish a heartbit in stdout (usefull if you collect it in a log/alerting management system such as elasticstack).

![kibana](./img/kibana.png)

It's also providing a `/v1/prom` http metrics endpoint that can be scrap by Prometheus:

![prometheus](./img/prometheus.png)

And can also send the metrics and some traces through OTLP/Grpc. Here's example of traces with Jaegger:

![jaegger](./img/jaegger.png)

## Table of content

[[_TOC_]]

## Git repositories

* Main repo: https://gitlab.comwork.io/oss/imalive
* Github mirror: https://github.com/comworkio/imalive.git
* Gitlab mirror: https://gitlab.com/ineumann/imalive.git

## Image on the dockerhub

The image is available and versioned here: https://hub.docker.com/r/comworkio/imalive-api

## Getting started

### Running with ansible

You can use this [ansible role](./ansible-imalive).

### Running with docker-compose

First create your `.env` file from the `.env.example`:

```shell
cp .env.example .env
```

Then replace the values (like the `IMALIVE_NODE_NAME` with your node name). Then:

```shell
$ docker compose up
```

You can check the API on [localhost:8080/docs](http://localhost:8080/docs) to see the Swagger docs.

### Running with K3D (Kubernetes / helm)

Use our helm chart [here](./helm)

#### Test with K3D (init the cluster)

```shell
k3d cluster create localdev --api-port 6550 -p "8089:80@loadbalancer"
sudo k3d kubeconfig get localdev > ~/.kube/config 
```

Continue to the next chapter

#### Install the helmchart

```shell
cd helm # all the commands below must be under imalive/helm directory
kubectl create ns imalive
helm dependency update
helm -n imalive install . -f values.yaml --generate-name
```

#### Check the deployment and ingress

```shell
kubectl -n imalive get deployments
kubectl -n imalive get pods
kubectl -n imalive get svc
kubectl -n imalive get ingress
curl localhost:8089 -v
```

## Endpoints

### Healthcheck

```shell
$ curl localhost:8080/v1/health
{"status": "ok", "time": "2021-11-05T06:55:28.274736", "alive": true, "name": "anode"}
```

### Manifests

```shell
$ curl localhost:8080/v1/manifest 
{"version": "1.0", "sha": "1c7cb1f", "arch": "x86"}
```

### Metrics

```shell
$ curl localhost:8080/v1/metrics
{"status": "ok", "disk_usage": {"total": 102.11687469482422, "used": 22.499202728271484, "free": 74.402099609375}, "virtual_memory": {"total": "1.9G", "available": "984.7M"}, "swap_memory": {"total": "1024.0M", "used": "493.1M", "free": "530.9M", "percent": 48.2}, "cpu": {"percent": {"all": i2.8, "percpu": [5.0, 4.0, 3.0, 2.0]}, "count": {"all": 4, "with_logical": 4}, "times": {"all": [10665.39, 7.0, 4718.91, 400345.0, 156.08, 0.0, 226.8, 0.0, 0.0, 0.0], "percpu": [[2488.92, 1.24, 1196.15, 100191.67, 38.08, 0.0, 82.3, 0.0, 0.0, 0.0], [2757.78, 1.63, 1196.16, 99992.0, 37.88, 0.0, 55.78, 0.0, 0.0, 0.0], [2704.56, 2.05, 1162.12, 100082.77, 40.01, 0.0, 47.75, 0.0, 0.0, 0.0], [2714.11, 2.06, 1164.46, 100078.54, 40.1, 0.0, 40.96, 0.0, 0.0, 0.0]]}}}
```

### Metrics for prometheus

If you want to use `imalive` as a Prometheus metrics exporter, this is the way:

```shell
$ curl localhost:8080/v1/prom
# HELP cpu_all cpu usage in percent
# TYPE cpu_all gauge
cpu_all 0.2
# HELP ram_total total of ram
# TYPE ram_total gauge
ram_total 5.1
# HELP ram_available available ram
# TYPE ram_available gauge
ram_available 4.4
# HELP disk_free free storage's space
# TYPE disk_free gauge
disk_free 43.546470642089844
# HELP disk_used used storage's space
# TYPE disk_used gauge
disk_used 12.563823699951172
# HELP disk_total total storage's space
# TYPE disk_total gauge
disk_total 56.096561431884766
# HELP imalive_imalive_http_reques
```

Here's an example of Prometheus config for scraping the data:

```yaml
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'imalive'
    static_configs:
      - targets: ['imalive-api:8080']
    metrics_path: '/v1/prom'
    scheme: http
```

## Heartbit

You can change the wait time between two heartbit with the `WAIT_TIME` environment variable (in seconds).

Here's an example of stdout heartbit:

```shell
INFO:root:{"status": "ok", "type": "heartbit", "name": "anode", "time": "2026-05-18T07:59:39.937657", "disk_usage": {"total": 17.367645263671875, "used": 11.47567367553711, "free": 5.891971588134766, "percent": 66.07501190469915}, "virtual_memory": {"total": "3.6G", "used": "2.0G", "available": "1.2G", "percent": 56.18330208023742, "numeric": {"total": 3831291904, "available": 1316343808, "used": 2152546304}}, "swap_memory": {"total": "0.0B", "used": "0.0B", "free": "0.0B", "percent": 0.0, "numeric": {"total": 0, "used": 0, "free": 0}}, "cpu": {"percent": {"all": 5.3, "percpu": [13.9, 8.8, 6.9]}, "count": {"all": 3, "with_logical": 3}, "times": {"all": [71694.12, 461.28, 33909.87, 2376653.45, 337.1, 0.0, 2976.5, 95573.14, 0.0, 0.0], "percpu": [[23453.39, 134.2, 11189.57, 792891.36, 109.86, 0.0, 1078.06, 33038.54, 0.0, 0.0], [23667.67, 151.29, 11193.59, 792279.17, 110.17, 0.0, 1123.32, 31956.51, 0.0, 0.0], [24573.05, 175.78, 11526.7, 791482.9, 117.06, 0.0, 775.12, 30578.08, 0.0, 0.0]]}}, "level": "INFO", "node": "cwcloud-ee-prod-v2-7pop40", "cid": "fc27e1c9-c939-4c9f-98d8-6f8f62cbcd17"}
```

You can change `anode` by your node name with the `IMALIVE_NODE_NAME` environment variable.

## OpenTelemetry

You can also configure an OTEL Grpc endpoint using the `OTEL_COLLECTOR_ENDPOINT` environment variable.

Here's an example of Prometheus configuration for scrapping the opentelemetry collector metrics:

```yaml
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'opentelemetry'
    static_configs:
      - targets: ['otel-collector:8889']
```

And the opentelemetry collector configuration as well for receiving the traces and metrics from imalive:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

exporters:
  logging:
  prometheus:
    endpoint: "0.0.0.0:8889"
    const_labels:
      otel: otel
  otlp:
    endpoint: "jaeger:4317"
    tls:
      insecure: true

processors:
  batch:

service:
  pipelines:
    metrics:
      receivers: [otlp]
      exporters: [prometheus]
    traces:
      receivers: [otlp]
      exporters: [otlp]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
```

## Monitor features

Imalive is also able to check some http endpoint and log and export metrics (status and duration).

In order to use that, just override the `/app/imalive.yml` with the following content:

```yaml
---
monitors:
  - type: http # only http and tcp are supported
    name: imalive
    url: http://localhost:8081 # if it's a tcp check, it must looks like host:port
    method: POST # optional (GET by default, only POST, PUT and GET are supported)
    body: '{"foo": "bar"}' # optional (body is ignored if method is GET)
    check_tls: false # optional (true by default)
    expected_http_code: "20*" # optional (20* by default), wildcard means "begin with"
    expected_contain: "\"status\":\"ok\"" # optional (no check on the body response if not present)
    timeout: 30 # optional (30 seconds if not present)
    username: changeit # optional (no basic auth if not present)
    password: changeit # optional (no basic auth if not present)
    level: INFO # optional, log level if monitor is healthy (DEBUG by default, only DEBUG and INFO are accepted)
    headers: # optional (no headers if empty)
      - name: Accept
        value: application/json
```

## Development / contributions

Go see this [documentation](./CONTRIBUTING.md)
