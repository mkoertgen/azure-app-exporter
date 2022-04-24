# Creating a Service Principal

We need a service principal for listing applications and their credential creation & expiration dates

```shell
# Create a service principal in the scope of your subscription
# AZURE_SUBSCRIPTION_ID: Your Azure subscription
$ az ad sp create-for-rbac -n "app-expiration-alerts" --role contributor --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID
{
  "appId": "***",
  "displayName": "app-expiration-alerts",
  "password": "***",
  "tenant": "***"
}

# Take note of the credentials
export AZURE_CLIENT_ID={appId}
export AZURE_CLIENT_SECRET={password}
export AZURE_TENANT_ID={tenant}
```

## Grant API Permissions

Next, we need to grant the service principal the API permissions `Application.ReadAll` to list other applications

```shell
# Find the service principal ids for reading applications: "Graph" and "Active Directory" (legacy, soon to be obsolete)
$ az ad sp list --query "[].{Name:appDisplayName, Id:appId}" --output table --all
Microsoft Graph                                               00000003-0000-0000-c000-000000000000
Windows Azure Active Directory                                00000002-0000-0000-c000-000000000000

# Graph
# Find API Permissions related for listing applications
$ az ad sp show --id 00000003-0000-0000-c000-000000000000 --query "appRoles[].{Value:value, Id:id}" --output table
Application.Read.All           9a5d68dd-52b0-4cc2-bd40-abcf44ac3a30
Application.ReadWrite.OwnedBy  18a4783c-866b-4cc7-a460-3d5e5662c884
Application.ReadWrite.All      1bfefb4e-e0b5-418b-a88f-73c46d2cc8e9
Directory.Read.All             7ab1d382-f21e-4acd-a863-ba3e13f7da61

# Add these permissions / roles to our service principal
$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000003-0000-0000-c000-000000000000 --api-permissions 9a5d68dd-52b0-4cc2-bd40-abcf44ac3a30=Role
#$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000003-0000-0000-c000-000000000000 --api-permissions 18a4783c-866b-4cc7-a460-3d5e5662c884=Role
#$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000003-0000-0000-c000-000000000000 --api-permissions 1bfefb4e-e0b5-418b-a88f-73c46d2cc8e9=Role
#$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000003-0000-0000-c000-000000000000 --api-permissions 7ab1d382-f21e-4acd-a863-ba3e13f7da61=Role

# Active Directory
# Find API Permissions related for listing applications
$ az ad sp show --id 00000002-0000-0000-c000-000000000000 --query "appRoles[].{Value:value, Id:id}" --output table
Application.Read.All           3afa6a7d-9b1a-42eb-948e-1650a849e176
Application.ReadWrite.All      1cda74f2-2616-4834-b122-5cb1b07f8a59
Application.ReadWrite.OwnedBy  824c81eb-e3f8-4ee6-8f6d-de7f50d565b7
Directory.Read.All             5778995a-e1bf-45b8-affa-663a9f3f4d04

# Add these permissions / roles to our service principal
$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000002-0000-0000-c000-000000000000 --api-permissions 3afa6a7d-9b1a-42eb-948e-1650a849e176=Role
#$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000002-0000-0000-c000-000000000000 --api-permissions 1cda74f2-2616-4834-b122-5cb1b07f8a59=Role
#$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000002-0000-0000-c000-000000000000 --api-permissions 824c81eb-e3f8-4ee6-8f6d-de7f50d565b7=Role
#$ az ad app permission add --id $AZURE_CLIENT_ID --api 00000002-0000-0000-c000-000000000000 --api-permissions 5778995a-e1bf-45b8-affa-663a9f3f4d04=Role

# Finally, grant admin-consent
$ az ad app permission admin-consent --id $AZURE_CLIENT_ID
```

## Finalize

```shell
# list application permissions
$ az ad app permission list --id $AZURE_CLIENT_ID
...
# login as app
$ az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
# and list applications including expiration dates
$ az ad app list --query "[].{appId:appId,credentials:passwordCredentials[].{name:customKeyIdentifier,created:startDate,expires:endDate}}"
[
  {
    "appId": "***",
    "credentials": [
      {
        "created": "2022-04-23T13:39:37.210801+00:00",
        "expires": "2023-04-23T13:39:37.210801+00:00",
        "name": "rbac"
      }
    ]
  }
]
```
