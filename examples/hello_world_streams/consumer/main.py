import asyncio

from rstream import (
    AMQPMessage,
    Consumer,
    ConsumerOffsetSpecification,
    MessageContext,
    OffsetType,
)

STREAM_NAME = "hello-python-stream"
STREAM_RETENTION = 5000000000


async def receive():
    async with Consumer(
        host="rabbitmq", username="guest", password="guest"
    ) as consumer:
        await consumer.create_stream(
            STREAM_NAME,
            exists_ok=True,
            arguments={"max-length-bytes": STREAM_RETENTION},
        )

        async def on_message(msg: AMQPMessage, message_context: MessageContext):
            stream = message_context.consumer.get_stream(
                message_context.subscriber_name
            )
            print("Got message: {} from stream {}".format(msg, stream))

        print("Press control + C to close")
        await consumer.start()
        offset_specification = ConsumerOffsetSpecification(OffsetType.FIRST, None)
        await consumer.subscribe(
            stream=STREAM_NAME,
            callback=on_message,
            offset_specification=offset_specification,
        )
        await consumer.run()


with asyncio.Runner() as runner:
    runner.run(receive())
