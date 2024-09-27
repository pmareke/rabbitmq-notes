import pika
from pika import BasicProperties, DeliveryMode


def send(message: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="task_queue", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=f"{message}",
        properties=BasicProperties(delivery_mode=DeliveryMode.Persistent),
    )
    print(f" [x] Sent '{message}'")
    connection.close()


for message in [
    "First message.",
    "Second message..",
    "Third message...",
    "Fourth message....",
    "Fifth message.....",
]:
    send(message)
