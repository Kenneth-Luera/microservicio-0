from rest_framework import serializers
from support.supportApp.models import Ticket, TicketHistory


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "status",
            "worker_id",
            "created_at",
            "updated_at"
        ]

        read_only_fields = [
            "id",
            "status",
            "worker_id",
            "created_at",
            "updated_at"
        ]

class TicketHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketHistory
        fields = "__all__"
        read_only_fields = "__all__"