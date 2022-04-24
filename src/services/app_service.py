from abc import abstractmethod
from typing import List

from models import AppRegistration


class AppService:
    @abstractmethod
    def get_all(self) -> List[AppRegistration]:
        pass

    @abstractmethod
    def get_by(self, app_id: str) -> AppRegistration:
        pass


