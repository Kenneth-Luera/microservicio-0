import uuid
from django.db import models


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user1_id = models.UUIDField()
    user2_id = models.UUIDField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user1_id", "user2_id"],
                name="unique_conversation_pair"
            )
        ]

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender_id = models.UUIDField()
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)