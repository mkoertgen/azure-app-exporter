from pydantic import BaseModel


class AppRegistration(BaseModel):
    id: str
