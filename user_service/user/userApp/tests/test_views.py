import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return _create_user


@pytest.fixture
def auth_client(client, create_user):
    user = create_user(username="test", email="test@test.com", password="123456")
    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_register_user(client):
    response = client.post("/api/register/", {
        "username": "ken",
        "email": "ken@test.com",
        "password": "Test1234!",
        "password2": "Test1234!"
    })

    assert response.status_code == 201


@pytest.mark.django_db
def test_get_user_data(auth_client):
    client, user = auth_client

    response = client.get("/api/me/")

    assert response.status_code == 200
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_internal_user_detail(client, create_user):
    user = create_user(username="ken", email="ken@test.com", password="123")

    response = client.get(f"/internal/users/{user.id}/")

    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_internal_user_not_found(client):
    response = client.get("/internal/users/00000000-0000-0000-0000-000000000000/")
    assert response.status_code == 404



@pytest.mark.django_db
def test_my_profile(auth_client):
    client, user = auth_client

    response = client.get("/api/profile/me/")  # 🔥 FIX

    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_detail(client, create_user):
    user = create_user(username="test", email="test@test.com", password="123")

    profile = user.profile 

    response = client.get(f"/profiles/{profile.id}/") 

    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_not_found(client):
    response = client.get("/profiles/00000000-0000-0000-0000-000000000000/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_list_profiles(client, create_user):
    create_user(username="test", email="test@test.com", password="123")

    response = client.get("/profiles/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_update_profile(auth_client):
    client, user = auth_client

    response = client.patch("/profile/update/", {
        "nickname": "nuevo_nick"
    })

    assert response.status_code == 200


@pytest.mark.django_db
def test_jwt_login(client, create_user):
    create_user(username="ken", password="123456")

    response = client.post("/api/login/", { 
        "username": "ken",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "access" in response.data