from django.db import models
import uuid


class Payment(models.Model):

    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    order_id = models.UUIDField()
    paypal_order_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)