[![azure-app-exporter](https://github.com/mkoertgen/azure-app-exporter/actions/workflows/azure-app-exporter.yml/badge.svg)](https://github.com/mkoertgen/azure-app-exporter/actions/workflows/azure-app-exporter.yml)

# azure-app-exporter

Exposing Prometheus Metrics for Azure App Registration useful for alerting on expiring Service Principal Credentials.

See [Documentation](_docs/index.md) for more information.

## Quick Start

Install using Docker of Helm (see `docker-compose.yml` or `./charts`).

The service authenticates against Azure using [Environmental Credentials](https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.environmentcredential?view=azure-python), i.e.

- AZURE_TENANT_ID: ID of the service principal's tenant. Also called its 'directory' ID.
- AZURE_CLIENT_ID: the application ID
- AZURE_CLIENT_SECRET: one of the service principal's client secrets

The Service Principal should have at least API permission `Application.Read.All` (Graph & Active Directory)

## TODOs

- Periodically update metrics by scraping `/apps`, e.g. using [Fast API - Repeated Tasks](https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/)
- Publish helm chart
