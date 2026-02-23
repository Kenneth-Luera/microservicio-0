import os
import django
import json
import pika
from payment.paymentApp.paypal_service import create_paypal_order

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payment.settings")
django.setup()

from payment.paymentApp.models import Payment


def callback(ch, method, properties, body):
    data = json.loads(body)

    print("Evento order_created recibido:")
    print(data)

    paypal_order = create_paypal_order(data["total_amount"])

    paypal_order_id = paypal_order["id"]

    approval_url = None
    for link in paypal_order["links"]:
        if link["rel"] == "approve":
            approval_url = link["href"]

    Payment.objects.create(
        order_id=data["order_id"],
        paypal_order_id=paypal_order_id,
        amount=data["total_amount"],
        status=Payment.Status.CREATED
    )

    print("PayPal Order ID:", paypal_order_id)
    print("Approval URL:", approval_url)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    channel = connection.channel()

    channel.queue_declare(queue="order_created", durable=True)

    channel.basic_consume(
        queue="order_created",
        on_message_callback=callback
    )

    print("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()