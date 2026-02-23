from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer
from .permissions import PublicReadAdminWrite

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [PublicReadAdminWrite]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            role = self.request.user.token.payload.get("role")
            if role == "admin":
                return Game.objects.all()

        return Game.objects.filter(is_active=True)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=204)
