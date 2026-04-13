import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from game.gameApp.models import Game

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
    user = create_user(username="user", password="Test1234!")

    class MockToken:
        payload = {"role": "user"}

    user.token = MockToken()

    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def admin_client(client, create_user):
    user = create_user(
        username="admin",
        password="Test1234!",
        is_staff=True,
        is_superuser=True
    )

    class MockToken:
        payload = {"role": "admin"}

    user.token = MockToken()

    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def create_game():
    def _create_game(**kwargs):
        return Game.objects.create(**kwargs)
    return _create_game


@pytest.mark.django_db
def test_list_games_public(client, create_game):
    create_game(title="Game 1", price=10, is_active=True)
    create_game(title="Game 2", price=20, is_active=False)

    response = client.get("/api/games/")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_list_games_admin(admin_client, create_game):
    client, _ = admin_client

    create_game(title="Game 1", price=10, is_active=True)
    create_game(title="Game 2", price=20, is_active=False)

    response = client.get("/api/games/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_create_game_admin(admin_client):
    client, _ = admin_client

    response = client.post("/api/games/", {
        "title": "New Game",
        "price": 50,
        "description": "Test game",
        "is_active": True
    })

    print(response.data)  # 👈 debug si algo falla

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_game_user_forbidden(auth_client):
    client, _ = auth_client

    response = client.post("/api/games/", {
        "title": "New Game",
        "price": 50
    })

    assert response.status_code in [403, 401]


@pytest.mark.django_db
def test_search_game(client, create_game):
    create_game(title="FIFA 24", price=10, is_active=True)
    create_game(title="Call of Duty", price=20, is_active=True)

    response = client.get("/api/games/?search=FIFA")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_filter_games(client, create_game):
    create_game(title="Game 1", price=10, is_active=True)
    create_game(title="Game 2", price=20, is_active=False)

    response = client.get("/api/games/?is_active=true")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_ordering_games(client, create_game):
    create_game(title="Game 1", price=30, is_active=True)
    create_game(title="Game 2", price=10, is_active=True)

    response = client.get("/api/games/?ordering=price")

    assert response.status_code == 200
    assert float(response.data[0]["price"]) == 10 


@pytest.mark.django_db
def test_soft_delete_game(admin_client, create_game):
    client, _ = admin_client

    game = create_game(title="Game 1", price=10, is_active=True)

    response = client.delete(f"/api/games/{game.id}/")

    print(response.data) 

    assert response.status_code == 204

    game.refresh_from_db()
    assert game.is_active is False


@pytest.mark.django_db
def test_delete_game_user_forbidden(auth_client, create_game):
    client, _ = auth_client

    game = create_game(title="Game 1", price=10, is_active=True)

    response = client.delete(f"/api/games/{game.id}/")

    assert response.status_code in [403, 401]