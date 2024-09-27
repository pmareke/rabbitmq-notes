import pika


def send(severity: str, message: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

    channel.basic_publish(
        exchange="direct_logs",
        routing_key=severity,
        body=f"{message}",
    )
    print(f" [x] Sent {severity}: '{message}'")
    connection.close()


for severity, message in [
    ("INFO", "First message."),
    ("ERROR", "Second message.."),
    ("INFO", "Third message..."),
    ("ERROR", "Fourth message...."),
    ("WARN", "Fifth message....."),
]:
    send(severity, message)
