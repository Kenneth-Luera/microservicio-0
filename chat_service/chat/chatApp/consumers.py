import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


@database_sync_to_async
def save_message(conversation_id, sender_id, message):

    from chat.chatApp.models import Message, Conversation

    conversation = Conversation.objects.get(id=conversation_id)

    Message.objects.create(
        conversation=conversation,
        sender_id=sender_id,
        content=message
    )


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user_id = self.scope.get("user_id")

        if not self.user_id:
            await self.close()
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data["message"]
        sender_id = self.user_id

        await save_message(
            self.conversation_id,
            sender_id,
            message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id
            }
        )


    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"]
        }))