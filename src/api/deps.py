from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient

from core.config import settings
from services.app_service import AzureAppService, AppService, MockAppService


def get_app_service() -> AppService:
    return AzureAppService(get_client()) if settings.azure_enabled else MockAppService()


def get_client() -> GraphClient:
    creds = EnvironmentCredential()
    return GraphClient(credential=creds)
