from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from support.supportApp.models import Ticket, TicketHistory
from support.supportApp.serializers import TicketSerializer
from support.supportApp.permissions import IsCustomer, IsWorker, IsAdmin


class CreateTicketView(APIView):

    permission_classes = [IsCustomer]

    def post(self, request):

        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            ticket = serializer.save(user_id=request.user.id)

            TicketHistory.objects.create(
                ticket=ticket,
                old_status="",
                new_status=Ticket.Status.OPEN,
                changed_by=request.user.id
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyTicketsView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):

        tickets = Ticket.objects.filter(user_id=request.user.id)
        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)
    
class AssignedTicketsView(APIView):
    permission_classes = [IsWorker]

    def get(self, request):

        tickets = Ticket.objects.filter(worker_id=request.user.id)
        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)
    
class AllTicketsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):

        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)
    
class TakeTicketView(APIView):

    permission_classes = [IsWorker]

    @transaction.atomic
    def patch(self, request, ticket_id):

        try:
            ticket = Ticket.objects.select_for_update().get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        if ticket.status != Ticket.Status.OPEN:
            return Response({"error": "Ticket already taken"}, status=400)

        old_status = ticket.status

        ticket.worker_id = request.user.id
        ticket.status = Ticket.Status.IN_PROGRESS
        ticket.save()

        TicketHistory.objects.create(
            ticket=ticket,
            old_status=old_status,
            new_status=Ticket.Status.IN_PROGRESS,
            changed_by=request.user.id
        )

        return Response({"message": "Ticket assigned"})