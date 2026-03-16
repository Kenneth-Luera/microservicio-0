from django.urls import path
from support.supportApp.views import (
    CreateTicketView,
    MyTicketsView,
    AssignedTicketsView,
    AllTicketsView,
    TakeTicketView
)

urlpatterns = [

    path("tickets/", CreateTicketView.as_view()),

    path("tickets/my/", MyTicketsView.as_view()),

    path("tickets/assigned/", AssignedTicketsView.as_view()),

    path("tickets/all/", AllTicketsView.as_view()),

    path("tickets/<uuid:ticket_id>/take/", TakeTicketView.as_view()),
]