import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)

        token = params.get("token")

        if token:
            token = token[0]  

            try:
                decoded_data = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                scope["user_id"] = decoded_data.get("user_id")

                print("DECODED:", decoded_data)
                print("USER_ID:", scope["user_id"])

            except Exception as e:
                print("JWT ERROR:", str(e))
                scope["user_id"] = None
        else:
            scope["user_id"] = None

        return await super().__call__(scope, receive, send)