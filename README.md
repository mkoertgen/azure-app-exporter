**NOTE: Public Archive. This project has been adopted by & transferred to [dodevops/azure-app-exporter](https://github.com/dodevops/azure-app-exporter)**

[![azure-app-exporter](https://github.com/mkoertgen/azure-app-exporter/actions/workflows/azure-app-exporter.yml/badge.svg)](https://github.com/mkoertgen/azure-app-exporter/actions/workflows/azure-app-exporter.yml)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/azure-app-exporter)](https://artifacthub.io/packages/search?repo=azure-app-exporter)

# azure-app-exporter

Exposing Prometheus Metrics for Azure App Registration useful for alerting on expiring Service Principal Credentials.

![Example Grafana Dashboard](_docs/img/grafana-dashboard.jpg)

See [Documentation](_docs/index.md) for more information.

Contribute on the [Project page](https://github.com/users/mkoertgen/projects/1/)

## Quick Start

Install using [Helm](https://artifacthub.io/packages/helm/azure-app-exporter/azure-app-exporter) or [Docker](https://github.com/mkoertgen/azure-app-exporter/pkgs/container/azure-app-exporter%2Fazure-app-exporter) and create a [Service Principal to use with Azure](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals).

The service authenticates against Azure using [Environmental Credentials](https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.environmentcredential?view=azure-python), i.e.

- AZURE_TENANT_ID: ID of the service principal's tenant. Also called its 'directory' ID.
- AZURE_CLIENT_ID: the application ID
- AZURE_CLIENT_SECRET: one of the service principal's client secrets

The Service Principal should have at least API permission `Application.Read.All` (Graph & Active Directory)
