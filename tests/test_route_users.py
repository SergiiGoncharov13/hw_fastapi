from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import status

import pytest

from src.database.models import Guest
from src.services.auth import auth_service

USER = {
    "firstname": "Unknown",
    "lastname": "Unknown",
    "email": "user@example.com",
    "phone": "+380001234567",
    "birthday": "2022-04-15",
    "additional_info": "nothing yet"
}


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)

    current_user: Guest = session.query(Guest).filter(Guest.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    data = response.json()
    return data["access_token"]


def test_create_user(client, token):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        response = client.post("/api/users", json=USER, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert "firstname" in data


def test_get_user(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get("/api/users", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["firstname"] == USER["firstname"]


def test_get_user_without_token(client):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.post(
            "/api/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_with_token(client, token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK


def test_get_user_error(client, token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.get("/api/users", headers={"Authorization": f"Bearer {token}"},)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Not found"


def test_update(client, token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.put("/api/user",
                              json=USER,
                              headers={"Authorization": f"Bearer {token}"},)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == USER["firstname"]


def test_update_error(client, token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.put("/api/users",
                              json=USER,
                              headers={"Authorization": f"Bearer {token}"},)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Not found"


def test_delete(client, token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.delete("/api/user", headers={"Authorization": f"Bearer {token}"},)
        assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_error(client, token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        response = client.delete("/api/users", headers={"Authorization": f"Bearer {token}"},)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Not found"
