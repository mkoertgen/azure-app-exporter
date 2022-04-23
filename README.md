[![azure-app-exporter](https://github.com/mkoertgen/azure-app-exporter/actions/workflows/azure-app-exporter.yml/badge.svg)](https://github.com/mkoertgen/azure-app-exporter/actions/workflows/azure-app-exporter.yml)

# azure-app-exporter

Exposing Prometheus Metrics for Azure Service Principals

## Why

As of now there is no straight option for automating alerts on expiring Credentials of [App Registrations](https://docs.microsoft.com/en-us/graph/notifications-integration-app-registration), especially not in a cloud native way (e.g. [Prometheus](https://prometheus.io/) metrics).
Some suggestions point towards Powershell or Runbook scripting (see references).
There are existing projects that map Azure metrics to Prometheus metrics, which is great.
However, since Azure does not provide metrics for App Registrations these options cannot work either.
Existing cloud native approaches out of initiatives like CrossPlane or Azure Service Operator also lack App Registrations.
Other IaC providers (e.g. Terraform) are not well suited for this task.

Finally, the [Microsoft Graph API Migration](https://docs.microsoft.com/en-us/graph/migrate-azure-ad-graph-faq) is an ongoing operation.

## How to use

The service authenticates against Azure using [Environmental Crednetials](https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.environmentcredential?view=azure-python), i.e.

- AZURE_TENANT_ID: ID of the service principal's tenant. Also called its 'directory' ID.
- AZURE_CLIENT_ID: the application ID
- AZURE_CLIENT_SECRET: one of the service principal's client secrets

## Requirements

- [Python >=3.10](https://www.python.org/)
- A Service Principal (again) to access Azure Applications

### Azure Preparation

```shell
# AZURE_SUBSCRIPTION_ID: Your Azure subscription
$ az ad sp create-for-rbac -n "app-expiration-alerts" --role contributor --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID
{
  "appId": "***",
  "displayName": "app-expiration-alerts",
  "password": "***",
  "tenant": "***"
}
```

#### API Permissions

```shell
$ az ad sp list --query "[].{Name:appDisplayName, Id:appId}" --output table --all
...
Microsoft Graph                                               00000003-0000-0000-c000-000000000000
Windows Azure Active Directory                                00000002-0000-0000-c000-000000000000
...
```

#### Microsoft Graph

```shell
# Show API Permissions
$ az ad sp show --id 00000003-0000-0000-c000-000000000000 --query "appRoles[].{Value:value, Id:id}" --output table | grep Application
...
Application.Read.All    9a5d68dd-52b0-4cc2-bd40-abcf44ac3a30

# Grant API Permissions
$ az ad app permission add --id %AZURE_CLIENT_ID% --api 00000003-0000-0000-c000-000000000000 --api-permissions 9a5d68dd-52b0-4cc2-bd40-abcf44ac3a30=Role
$ az ad app permission grant --id ... --api 00000003-0000-0000-c000-000000000000

```

#### Azure Active Directory (Legacy)

```shell
# Show API Permissions
$ az ad sp show --id 00000002-0000-0000-c000-000000000000 --query "appRoles[].{Value:value, Id:id}" --output table
...
Application.Read.All    3afa6a7d-9b1a-42eb-948e-1650a849e176

# Grant API Permissions
$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000002-0000-0000-c000-000000000000 --api-permissions 3afa6a7d-9b1a-42eb-948e-1650a849e176=Role
The underlying Active Directory Graph API will be replaced by Microsoft Graph API in Azure CLI 2.37.0. Please carefully review all breaking changes introduced during this migration: https://docs.microsoft.com/cli/azure/microsoft-graph-migration
Invoking "az ad app permission grant --id ... --api 00000002-0000-0000-c000-000000000000" is needed to make the change effective

$ az ad app permission grant --id ... --api 00000002-0000-0000-c000-000000000000
{
...
  "startTime": "2022-04-23T14:19:13.171302"
}
```

### Final Test

```shell
$ az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
$ az ad app list
```

## Development

```shell
# Install dependencies
pip install --user -r requirements.txt -r requirements-dev.txt

# Update dependencies
$ python -m pur -r requirements.txt -r requirements-dev.txt
All requirements up-to-date.

# Run tests
$ python -m pytest --cov
tests\api\test_sp.py .                                           [100%]

============================= 1 passed in 0.05s =============================

# Run - development mode
$ python -m uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['...azure-app-exporter/src']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [3272] using statreload
WARNING:  The --reload flag should not be used in production.
INFO:     Started server process [20152]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Next hit

- API: [/api/openapi.json](http://localhost:8000/api/openapi.json) & Swagger-UI at [/docs]](http://localhost:8000/docs)
- Metrics: [/health](http://localhost:8000/health) & [/metrics](http://localhost:8000/metrics)

## Azure CLI

Kind of reverse engineering the Microsoft Graph API it is helpful to observe what the Azure CLI is doing under the hood, e.g.

```shell
$ az ad sp credential list --id $AZURE_CLIENT_ID --debug
...
# Find Service Principal by App Id (or Name) to get {sp_id} ...
msrest.http_logger: Request URL: 'https://graph.windows.net/.../servicePrincipals?$filter=servicePrincipalNames/any(c:c eq '{app_id}')'
# Retreive the Service Principal
msrest.http_logger: Request URL: '.../servicePrincipals/{sp_id}'
# Retreive application by appId
msrest.http_logger: Request URL: '/applications?$filter=appId eq {app_id}'
# Retreive credentials by application ${object_id}
msrest.http_logger: Request URL: '/applications/{object_id}/passwordCredentials
```

## References

- [Supported metrics with Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/metrics-supported)
- [Microsoft Graph Core Python Client Library (preview)](https://github.com/microsoftgraph/msgraph-sdk-python-core)
- [Azure Identity client library for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)
- [az ad sp credential list](https://docs.microsoft.com/de-de/cli/azure/ad/sp/credential?view=azure-cli-latest#az-ad-sp-credential-list)
- [List servicePrincipals](https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list?view=graph-rest-1.0&tabs=http)
- [Azure AD & Microsoft Graph permission scopes, with Azure CLI](https://www.agrenpoint.com/azcli-adscope/)

### Honorable mentions

- [How can I tell when a Azure AD client secret expires?](https://stackoverflow.com/questions/44075464/how-can-i-tell-when-a-azure-ad-client-secret-expires)
- [Alert on Client Secret Key Expiry for App registration](https://social.msdn.microsoft.com/Forums/office/en-US/f834ed27-a792-496d-93be-7ece9cbcd212/alert-on-client-secret-key-expiry-for-app-registration?forum=WindowsAzureAD)
- [Security Graph API and getting alerts](https://msandbu.org/security-graph-api-and-getting-alerts/)
- [Azure/azure-service-operator](https://github.com/Azure/azure-service-operator) for Kubernetes

#### Prometheus & Grafana, ...

- [webdevops/azure-metrics-exporter](https://github.com/webdevops/azure-metrics-exporter) - great, maps to Azure metrics to Prometheus metrics. However App registrations have no metrics
- [RobustPerception/azure_metrics_exporter](https://github.com/RobustPerception/azure_metrics_exporter) - againa: resources only, no apps
- Grafana [Azure Monitor data source](https://grafana.com/docs/grafana/latest/datasources/azuremonitor/) has no option for app registrations or service principals
- Reading [Application](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/application) details using [Terraform](https://www.terraform.io/)
