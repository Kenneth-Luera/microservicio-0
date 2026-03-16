from django.urls import path
from .views import CreateConversationView

urlpatterns = [
    path("conversations/create/", CreateConversationView.as_view()),
]