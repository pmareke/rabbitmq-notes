import os

import pika


def receive() -> None:
    severity = os.getenv("SEVERITY", "info")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange="direct_logs", routing_key=severity, queue=queue_name)
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
