import pika
import json


def publish_event(queue_name, message):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()
