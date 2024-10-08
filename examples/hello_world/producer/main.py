import pika


def send(name: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    channel.basic_publish(exchange="", routing_key="hello", body=f"Hello {name}!")
    print(f" [x] Sent 'Hello {name}!'")
    connection.close()


for name in ["Alice", "Bob", "Katherine", "Peter", "Michael"]:
    send(name)
