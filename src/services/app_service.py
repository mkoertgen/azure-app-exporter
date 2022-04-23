from msgraph.core import GraphClient

from models import AppRegistration


class AppService:
    def get(self, app_id: str) -> AppRegistration:
        return AppRegistration(id=app_id)


class AzurePrincipalService(AppService):
    def __int__(self, client: GraphClient):
        self.client = client

    def get(self, app_id: str) -> AppRegistration:
        result = self.client.get(f"/servicePrincipals?$filter=servicePrincipalNames/any(c:c eq '{app_id}')")
        app = result.json()['value'][0]
        print(app)
        return AppRegistration(id=app_id)
