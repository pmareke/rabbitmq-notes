from threading import Thread
from time import sleep

import pika


def hello_world() -> None:
    print("Starting hello world example")
    thread1 = Thread(target=receive)
    thread1.start()
    sleep(1)
    send()


def send() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    print(" [x] Sent 'Hello World!'")
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


if __name__ == "__main__":
    hello_world()
