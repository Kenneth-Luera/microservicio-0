import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat.chatApp.routing import websocket_urlpatterns
from chat.chatApp.jwt_middleware import JWTAuthMiddleware


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})