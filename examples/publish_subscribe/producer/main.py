import pika


def send(message: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    channel.basic_publish(exchange="logs", routing_key="", body=f"{message}")
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
