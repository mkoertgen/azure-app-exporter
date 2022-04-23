from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from models import AppRegistration
from services.app_service import AppService

from api import deps

router = InferringRouter()


@cbv(router)
class AppsController:
    service: AppService = Depends(deps.get_app_service)

    @router.get("/{app_id}")
    def get(self, app_id: str) -> AppRegistration:
        return self.service.get(app_id)
