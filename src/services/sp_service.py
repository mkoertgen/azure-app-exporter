from models import ServicePrincipal


class PrincipalService:
    def get_principal(self, sp_id: str) -> ServicePrincipal:
        return ServicePrincipal(id=sp_id)
