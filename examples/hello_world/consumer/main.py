import pika
from pika.channel import Channel
from pika.spec import Basic, BasicProperties


def receive() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    def _callback(
        channel: Channel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        print(f" [x] Received {body}")

    channel.basic_consume(queue="hello", on_message_callback=_callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()


receive()
