# Contributions

For the developers you can test your changes on the app by running this command:

```shell
docker compose -f docker-compose-local.yml up --build --force-recreate
```

You can also run unit tests by running this command:

```shell
docker compose -f docker-compose-local.yml up --build --abort-on-container-exit imalive-tests
```

Then you can try:
* the api endpoint: http://localhost:8080
* jaegger UI here for the traces: http://localhost:16686
* the opentelemetry metrics exporter endpoint: http://localhost:8889/metrics
* prometheus: http://localhost:9090
