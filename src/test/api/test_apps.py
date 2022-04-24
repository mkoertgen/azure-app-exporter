from fastapi.testclient import TestClient

from core.config import settings
from models import AppRegistration
from services.app_service import MockAppService


def test_apps(client: TestClient):
    path = f"{settings.api_base}/apps"
    expected = MockAppService.SOME_APP

    response = client.get(f"{path}")
    assert response.ok
    assert len(response.json()) == 1
    actual = AppRegistration.parse_obj(response.json()[0])
    assert actual == expected

    response = client.get(f"{path}/{expected.id}")
    assert response.ok
    actual = AppRegistration.parse_obj(response.json())
    assert actual == expected
