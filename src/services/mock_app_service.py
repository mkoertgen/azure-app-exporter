from typing import Dict, List

from models import AppRegistration
from services.app_service import AppService


class MockAppService(AppService):
    SOME_APP = AppRegistration(id="57886480-166a-473d-b7f2-90382e4b654a", name="some-app", credentials=[])
    apps: Dict[str, AppRegistration] = {}

    def __init__(self, apps: Dict[str, AppRegistration] = None):
        if apps:
            self.apps = apps
        else:
            self.apps[MockAppService.SOME_APP.id] = MockAppService.SOME_APP

    async def get_all(self) -> List[AppRegistration]:
        return list(self.apps.values())

    async def get_by(self, app_id: str) -> AppRegistration:
        return self.apps[app_id]
