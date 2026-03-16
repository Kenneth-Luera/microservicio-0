import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_string = scope["query_string"].decode()

        params = parse_qs(query_string)

        token = params.get("token")

        if token:
            token = token[0]

            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                scope["user_id"] = payload["user_id"]

            except jwt.InvalidTokenError:
                scope["user_id"] = None

        else:
            scope["user_id"] = None

        return await super().__call__(scope, receive, send)