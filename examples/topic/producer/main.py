import pika


def send(routing_key: str, message: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

    channel.basic_publish(
        exchange="topic_logs",
        routing_key=routing_key,
        body=f"{message}",
    )
    print(f" [x] Sent {routing_key}: '{message}'")
    connection.close()


send("kern.critical", "A critical kernel error")
send("kern.log", "A log kernel trace")
send("foo.bar.zoo", "No idea what this is")
