from abc import abstractmethod
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

import dateutil.parser
from fastapi import HTTPException
from msgraph.core import GraphClient

from models import AppRegistration
from models.app_registration import Credential


class AppService:
    @abstractmethod
    def get_all(self) -> List[AppRegistration]:
        pass

    @abstractmethod
    def get_by(self, app_id: str) -> AppRegistration:
        pass


class MockAppService(AppService):
    SOME_APP = AppRegistration(id="57886480-166a-473d-b7f2-90382e4b654a", name="some-app", credentials=[])
    apps: Dict[str, AppRegistration] = {}

    def __init__(self, apps: Dict[str, AppRegistration] = None):
        if apps:
            self.apps = apps
        else:
            self.apps[MockAppService.SOME_APP.id] = MockAppService.SOME_APP

    def get_all(self) -> List[AppRegistration]:
        return list(self.apps.values())

    def get_by(self, app_id: str) -> AppRegistration:
        return self.apps[app_id]


class AzureAppService(AppService):
    def __init__(self, client: GraphClient):
        self.client = client

    def get_all(self) -> List[AppRegistration]:
        result = self.client.get("/applications")
        if not result.ok:
            raise HTTPException(status_code=result.status_code)
        value = result.json()['value']
        apps = [AzureAppService._map_app(a) for a in value]
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
        creds = [AzureAppService._map_cred(c) for c in dct['passwordCredentials']]
        return AppRegistration(id=app_id, name=name, credentials=creds)

    @staticmethod
    def _map_cred(dct: Dict) -> Credential:
        # https://stackoverflow.com/a/71778150/2592915
        return Credential(
            name=dct['customKeyIdentifier'],
            created=dateutil.parser.isoparse(dct['startDateTime']),
            expires=dateutil.parser.isoparse(dct['endDateTime'])
        )
