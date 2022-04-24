from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Credential(BaseModel):
    name: Optional[str]
    created: Optional[datetime]
    expires: Optional[datetime]


class AppRegistration(BaseModel):
    id: str
    name: str
    credentials: List[Credential]
