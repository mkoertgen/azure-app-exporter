from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from models import ServicePrincipal
from services.sp_service import PrincipalService

from api import deps

router = InferringRouter()


@cbv(router)
class PrincipalsController:
    service: PrincipalService = Depends(deps.get_principal_service)

    @router.get("/{sp_id}")
    def get(self, sp_id: str) -> ServicePrincipal:
        return self.service.get_principal(sp_id)
