import uuid
from django.db import models,transaction


class Ticket(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user_id = models.UUIDField()
    worker_id = models.UUIDField(null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
    
@transaction.atomic
def take_ticket(ticket_id, worker_id):

    ticket = Ticket.objects.select_for_update().get(id=ticket_id)

    if ticket.status != Ticket.Status.OPEN:
        raise Exception("Ticket ya fue tomado")

    ticket.worker_id = worker_id
    ticket.status = Ticket.Status.IN_PROGRESS
    ticket.save()
    
class TicketHistory(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="history"
    )

    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)

    changed_by = models.UUIDField()

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.id} {self.old_status} → {self.new_status}"