import pika


def consume() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    def _callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue="hello", on_message_callback=_callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()


consume()
