from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_view() -> None:
    name = "Vadim"
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    expected_response = f"Hello {name}!"
    response_data = response.json()
    assert expected_response == response_data["message"], response_data
