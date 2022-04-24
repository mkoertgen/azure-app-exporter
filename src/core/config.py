from pydantic import BaseSettings


class Settings(BaseSettings):
    api_base: str = "/api"
    project_name: str = 'azure-app-exporter'
    azure_enabled: bool = False


settings = Settings()
