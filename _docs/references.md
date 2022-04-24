# References

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

## Links

- [Supported metrics with Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/metrics-supported)
- [Microsoft Graph Core Python Client Library (preview)](https://github.com/microsoftgraph/msgraph-sdk-python-core)
- [Azure Identity client library for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)
- [az ad sp credential list](https://docs.microsoft.com/de-de/cli/azure/ad/sp/credential?view=azure-cli-latest#az-ad-sp-credential-list)
- [List servicePrincipals](https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list?view=graph-rest-1.0&tabs=http)
- [Azure AD & Microsoft Graph permission scopes, with Azure CLI](https://www.agrenpoint.com/azcli-adscope/)
- [Creating a Self-Signed Certificate With OpenSSL](https://www.baeldung.com/openssl-self-signed-cert)

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
