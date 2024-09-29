import os

import pika


def receive() -> None:
    routing_key = os.getenv("ROUTING_KEY", "*")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange="topic_logs",
        routing_key=routing_key,
        queue=queue_name,
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")

    def _callback(ch, method, properties, body: bytes):
        print(f" [x] Received {method.routing_key}: {body.decode()}")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=_callback,
        auto_ack=True,
    )

    channel.start_consuming()


receive()
