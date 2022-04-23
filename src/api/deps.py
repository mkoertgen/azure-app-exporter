from azure.identity import EnvironmentCredential, ClientSecretCredential, DefaultAzureCredential
from msgraph.core import GraphClient

from services.app_service import AppService, AzurePrincipalService


def get_app_service() -> AppService:
    # return PrincipalService()
    return AzurePrincipalService(get_client())


def get_client() -> GraphClient:
    credentials = EnvironmentCredential()
    return GraphClient(credential=credentials, scopes=["https://graph.windows.net//.default"])

