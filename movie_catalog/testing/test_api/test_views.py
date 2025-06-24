import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_view() -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    expected_response = "Hello Guest!"
    response_data = response.json()
    assert expected_response == response_data["message"], response_data


@pytest.mark.parametrize(
    "name",
    [
        "Vadim",
        "",
        "Petr Ivanov",
        "Ivan!$%^£",
    ],
)
def test_root_view_custom_name(name: str) -> None:
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    expected_response = f"Hello {name}!"
    response_data = response.json()
    assert expected_response == response_data["message"], response_data
