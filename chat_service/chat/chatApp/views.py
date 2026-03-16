from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.chatApp.models import Conversation


class CreateConversationView(APIView):

    def post(self, request):

        user1 = request.data.get("user1_id")
        user2 = request.data.get("user2_id")

        conversation = Conversation.objects.filter(
            user1_id=user1,
            user2_id=user2
        ).first()

        if not conversation:
            conversation = Conversation.objects.filter(
                user1_id=user2,
                user2_id=user1
            ).first()

        if not conversation:
            conversation = Conversation.objects.create(
                user1_id=user1,
                user2_id=user2
            )

        return Response({
            "conversation_id": str(conversation.id)
        }, status=status.HTTP_200_OK)