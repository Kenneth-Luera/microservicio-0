from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from game.gameApp.views import GameViewSet


router = DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
