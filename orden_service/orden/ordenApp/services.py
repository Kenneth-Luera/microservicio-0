import requests
from django.conf import settings


def get_game_details(game_id):

    url = f"{settings.GAME_SERVICE_URL}{game_id}/"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None
