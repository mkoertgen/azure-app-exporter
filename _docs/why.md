# Why

As of now there is no straight option for automating alerts on expiring Credentials of [App Registrations](https://docs.microsoft.com/en-us/graph/notifications-integration-app-registration), especially not in a cloud native way (e.g. [Prometheus](https://prometheus.io/) metrics).
Some suggestions point towards Powershell or Runbook scripting (see references).
There are existing projects that map Azure metrics to Prometheus metrics, which is great.
However, since Azure does not provide metrics for App Registrations these options cannot work either.
Existing cloud native approaches out of initiatives like CrossPlane or Azure Service Operator also lack App Registrations.
Other IaC providers (e.g. Terraform) are not well suited for this task.

Finally, the [Microsoft Graph API Migration](https://docs.microsoft.com/en-us/graph/migrate-azure-ad-graph-faq) is an ongoing operation.
