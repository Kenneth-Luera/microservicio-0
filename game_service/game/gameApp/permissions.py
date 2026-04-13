from rest_framework.permissions import BasePermission, SAFE_METHODS


class PublicReadAdminWrite(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        token = getattr(request.user, "token", None)

        if not token:
            return False

        payload = getattr(token, "payload", {})

        role = payload.get("role")
        status = payload.get("status", "active")

        return role == "admin" and status == "active"