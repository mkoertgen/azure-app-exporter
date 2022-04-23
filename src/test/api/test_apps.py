from fastapi.testclient import TestClient

from core.config import settings
from models import AppRegistration


def test_sp(client: TestClient):
    path = f"{settings.API_BASE}/sp"
    expected = AppRegistration(id='ae9244e5-5505-439b-99b4-0346ded9562d')

    response = client.get(f"{path}/{expected.id}")
    assert response.ok
    actual = AppRegistration.parse_obj(response.json())
    assert actual == expected
