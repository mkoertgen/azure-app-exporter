from datetime import datetime
from typing import List, Optional

from msgraph.generated.models.application import Application
from msgraph.generated.models.key_credential import KeyCredential
from msgraph.generated.models.password_credential import PasswordCredential
from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
from msgraph.graph_service_client import GraphServiceClient
from prometheus_client import Gauge

from models import AppRegistration
from models.app_registration import Credential
from services.app_service import AppService

APP_EXPIRY = Gauge(
    "azure_app_earliest_expiry",
    "Returns earliest credential expiry in unix time (seconds)",
    ["app_id", "app_name"]
)

APP_CREDS_EXPIRY = Gauge(
    "azure_app_credential_expiry",
    "Returns the expiration in unix time (seconds) for each credential of an app",
    ["app_id", "app_name", "credential_name"]
)


class AzureAppService(AppService):
    def __init__(self, client: GraphServiceClient):
        self.client = client

    async def get_all(self) -> List[AppRegistration]:
        result = await self.client.applications.get()
        apps = []
        while result is not None:
            apps += [await self._map_app(a) for a in result.value]
            if result.odata_next_link is None:
                break
            result = await self.client.applications.with_url(result.odata_next_link).get()

        self.observe(apps)
        return apps

    async def get_by(self, app_id: str) -> AppRegistration:
        result = await self.client.applications.by_application_id(app_id).get()
        if result is not None:
            return await self._map_app(result)
        else:
            raise "Application with app id %s not found." % app_id

    async def _map_app(self, app: Application) -> AppRegistration:
        app_id = app.app_id
        name = app.display_name
        sp_creds = await self._fetch_sp_creds(app_id)
        creds = []
        for cred in app.password_credentials + app.key_credentials + sp_creds:
            if len([c for c in creds if c.name == cred.display_name]) == 0:
                creds.append(self._map_cred(cred))
        return AppRegistration(id=app_id, name=name, credentials=creds)

    async def _fetch_sp_creds(self, app_id):
        query_params = ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetQueryParameters(
            search=f'\"appId:{app_id}\"'
        )
        request_configuration = ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetRequestConfiguration(
            query_parameters=query_params,
        )
        request_configuration.headers.add("ConsistencyLevel", "eventual")
        response = await self.client.service_principals.get(request_configuration=request_configuration)
        sp_creds = []
        if len(response.value) > 0:
            sp_creds = response.value[0].key_credentials + response.value[0].password_credentials
        return sp_creds

    @staticmethod
    def _map_cred(cred: KeyCredential | PasswordCredential) -> Credential:
        return Credential(
            name=cred.display_name,
            created=cred.start_date_time,
            expires=cred.end_date_time
        )

    @staticmethod
    def observe(apps: List[AppRegistration]):
        APP_EXPIRY.clear()
        APP_CREDS_EXPIRY.clear()
        for app in apps:
            if len(app.credentials) > 0:
                expiry: Optional[datetime] = min(map(lambda c: c.expires, app.credentials))
                if expiry:
                    APP_EXPIRY.labels(app_id=app.id, app_name=app.name).set(int(expiry.timestamp()))
                for cred in app.credentials:
                    (
                        APP_CREDS_EXPIRY
                        .labels(app_id=app.id, app_name=app.name, credential_name=cred.name)
                        .set(int(cred.expires.timestamp()))
                     )
