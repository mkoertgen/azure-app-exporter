# azure-sp-exporter

Exposing Prometheus Metrics for Azure Service Principals

## Requirements

- [Python >=3.10](https://www.python.org/)

## Development

```shell
# Install Dependencies
pip install --user -r requirements.txt -r requirements-dev.txt

# Run
$ uvicorn main:app [--reload]
INFO:     Started server process [13728]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

# Tests
$ pytest
tests\api\test_sp.py .                                           [100%]

============================= 1 passed in 0.05s =============================
```

Next hit

- API: [/api/openapi.json](http://localhost:8000/api/openapi.json) & Swagger-UI at [/docs]](http://localhost:8000/docs)
- Metrics: [/health](http://localhost:8000/health) & [/metrics](http://localhost:8000/metrics)

## References

- [az ad sp credential list](https://docs.microsoft.com/de-de/cli/azure/ad/sp/credential?view=azure-cli-latest#az-ad-sp-credential-list)
- [List servicePrincipals](https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list?view=graph-rest-1.0&tabs=http)
