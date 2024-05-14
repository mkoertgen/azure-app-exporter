from datetime import datetime
from typing import List, Dict, Optional

import dateutil.parser
from fastapi import HTTPException
from msgraph.core import GraphClient
from prometheus_client import Gauge
from prometheus_client import REGISTRY

from models import AppRegistration
from models.app_registration import Credential
from services.app_service import AppService

APP_EXPIRY = Gauge(
    "azure_app_earliest_expiry",
    "Returns earliest credential expiry in unix time (seconds)",
    ["app_id","app_name"]
)

APP_CREDS_EXPIRY = Gauge(
    "azure_app_credential_expiry",
    "Returns the expiration in unix time (seconds) for each credential of an app",
    ["app_id", "app_name", "credential_name"]
)

class AzureAppService(AppService):
    def __init__(self, client: GraphClient):
        self.client = client

    def get_all(self) -> List[AppRegistration]:
        result = self.client.get("/applications")
        if not result.ok:
            raise HTTPException(status_code=result.status_code)
        value = result.json()['value']
        apps = [AzureAppService._map_app(a) for a in value]
        self.observe(apps)
        return apps

    def get_by(self, app_id: str) -> AppRegistration:
        result = self.client.get(f"/applications?$filter=appId eq '{app_id}'")
        if not result.ok:
            raise HTTPException(status_code=result.status_code)
        return AzureAppService._map_app(result.json()['value'][0])

    @staticmethod
    def _map_app(dct: Dict) -> AppRegistration:
        app_id = dct['appId']
        name = dct['displayName']
        creds = [AzureAppService._map_cred(c) for c in dct['passwordCredentials']+dct['keyCredentials']]
        return AppRegistration(id=app_id, name=name, credentials=creds)

    @staticmethod
    def _map_cred(dct: Dict) -> Credential:
        # https://stackoverflow.com/a/71778150/2592915
        return Credential(
            name=dct['displayName'],
            created=dateutil.parser.isoparse(dct['startDateTime']),
            expires=dateutil.parser.isoparse(dct['endDateTime'])
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
                    APP_CREDS_EXPIRY.labels(app_id=app.id, app_name=app.name, credential_name=cred.name).set(
                        int(cred.expires.timestamp()))
