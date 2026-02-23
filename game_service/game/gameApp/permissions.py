from rest_framework.permissions import BasePermission, SAFE_METHODS

class PublicReadAdminWrite(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        role = request.user.token.payload.get("role")
        status = request.user.token.payload.get("status")

        return role == "admin" and status == "active"
