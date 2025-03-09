# rock-spawner

OBiBa/Rock server pod spawner in a Kubernetes environment. This application runs and manages on-demand Rock servers, for single client usage. Allows K8s cluster to use minimal resources, and to always start a R session from a clean environment.

## Development

```sh
make install
make run
```

Then connect to http://localhost:8086/docs to get the API documentation.

## Environment Variables

```sh
# Service authentication key
API_KEYS=changeme

# Kubernetes variables
# ...
```