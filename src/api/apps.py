from typing import List

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from models import AppRegistration
from services.mock_app_service import MockAppService

from api import deps

router = InferringRouter()


@cbv(router)
class AppsController:
    service: MockAppService = Depends(deps.get_app_service)

    @router.get("/")
    def get_all(self) -> List[AppRegistration]:
        return self.service.get_all()

    @router.get("/{app_id}")
    def get_by(self, app_id: str) -> AppRegistration:
        return self.service.get_by(app_id)
