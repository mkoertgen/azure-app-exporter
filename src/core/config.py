from typing import Any, Dict, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_BASE: str = "/api"
    PROJECT_NAME: str = 'azure-sp-metrics-exporter'

    @staticmethod
    def get_project_name(v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    class Config:
        case_sensitive = True


settings = Settings()
