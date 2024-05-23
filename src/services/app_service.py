from abc import abstractmethod
from typing import List

from models import AppRegistration


class AppService:
    @abstractmethod
    async def get_all(self) -> List[AppRegistration]:
        pass

    @abstractmethod
    async def get_by(self, app_id: str) -> AppRegistration:
        pass


