from azure.identity import EnvironmentCredential
from msgraph.graph_service_client import GraphServiceClient

from core.config import settings
from services.app_service import AppService
from services.azure_app_service import AzureAppService
from services.mock_app_service import MockAppService


def get_app_service() -> AppService:
    return AzureAppService(get_client()) if settings.azure_enabled else MockAppService()


def get_client() -> GraphServiceClient:
    creds = EnvironmentCredential()
    # GraphServiceClient works with EnvironmentCredential just as well
    # noinspection PyTypeChecker
    return GraphServiceClient(credentials=creds)
