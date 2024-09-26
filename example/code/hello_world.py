from threading import Thread

import pika


def hello_world() -> None:
    thread1 = Thread(target=receive)
    thread1.start()

    for name in ["Alice", "Bob", "Katherine", "Peter", "Michael"]:
        send(name)


def send(name: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    channel.basic_publish(exchange="", routing_key="hello", body=f"Hello {name}!")
    print(f" [x] Sent 'Hello {name}!'")
    connection.close()


def receive() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    channel.basic_consume(queue="hello", on_message_callback=_callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def _callback(ch, method, properties, body):
    print(f" [x] Received {body}")


hello_world()
