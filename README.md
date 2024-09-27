# RabbitMQ

- One broker to queue them all.
- RabbitMQ is a reliable and mature messaging and streaming broker.

## AMQP 0-9-1

- AMQP 0-9-1 (`Advanced Message Queuing Protocol`) is a messaging protocol.
- Messaging `brokers` receive messages from `publishers` and `route` them to `consumers`.
- The model has a notion of message `acknowledgements`, when a message is delivered to 
a consumer the consumer notifies the broker.
    - `Publishers` choose how to handle situations like this by publishing messages using certain parameters.

### Exchanges

- `Messages` are published to `exchanges`.
- Then the broker either deliver messages to consumers subscribed to queues, or 
consumers fetch/pull messages from queues on demand.
- `Exchanges` then distribute message copies to queues using rules called `bindings`.
- `Exchanges` are AMQP 0-9-1 entities where messages are sent to.
- `Exchanges` take a message and route it into zero or more queues.
- `Exchanges` are declared with a number of attributes, the most important of which are:
    - `Name`.
    - `Durability` (exchanges survive broker restart).
    - `Auto-delete` (exchange is deleted when last queue is unbound from it).
    - `Arguments` (optional, used by plugins and broker-specific features).
- `Exchanges` can be durable or transient:
    - `Durable` exchanges survive broker restart.
    - `Transient` exchanges do not.
- The `default exchange` is a direct exchange with no name pre-declared by the broker.
    - Very useful for simple applications.
    - Every queue that is created is automatically bound to it with a routing key which is the same as the queue name.
- A `direct exchange` delivers messages to queues based on the message routing key.
    - It's ideal for the unicast routing of messages.
- A `fanout exchange` routes messages to all of the queues that are bound to it and the routing key is ignored.
- `Topic exchanges` route messages to one or many queues based on matching between a message routing key and the 
pattern that was used to bind a queue to an exchange.
    - They are commonly used for the multicast routing of messages.

### Queues

- They store messages that are consumed by applications.
- `Queues` have some properties:
    - `Name`.
    - `Durable` (the queue will survive a broker restart).
    - `Exclusive` (used by only one connection and the queue will be deleted when that connection closes).
    - `Auto-delete` (queue that has had at least one consumer is deleted when last consumer unsubscribes).
    - `Arguments` (optional; used by plugins and broker-specific features such as message TTL, queue length limit, etc).

### Bindings

- They are `rules` that `exchanges` use to route `messages` to `queues`.

### Consumers

- Applications have to indicate interest in consuming messages from a particular queue.
- Each `consumer` (subscription) has an identifier called a consumer tag.

### Message Acknowledgements

-  There are two `acknowledgement` modes:
    - After `broker` sends a message to an application (using either basic.deliver or basic.get-ok method).
    - After the `application` sends back an acknowledgement (using the basic.ack method).
- The former choice is called the automatic acknowledgement model, while the latter is 
called the explicit acknowledgement model.
- If a `consumer` dies without sending an acknowledgement, the `broker` will redeliver it to another consumer.

### Message Attributes and Payload

- `Messages` in the AMQP 0-9-1 model have attributes:
    - Content type.
    - Content encoding.
    - Routing key.
    - Delivery mode (persistent or not).
    - Message priority.
    - Message publishing timestamp.
    - Expiration period.
    - Publisher application id.

## How to Use RabbitMQ

### Publishers

- `Publishers` are often long lived.
- `Publishers` usually open their connection(s) during application startup.
- `Routing` in AMQP 0-9-1 is performed by exchanges.
    - `Exchanges` are named routing tables.
    - `Table` entries are called bindings.
- There are several built-in exchange `types`:
    - Topic.
    - Fanout.
    - Direct (including the default exchange).
    - Headers.

### Consumers

- `Consumers` are meant to be long lived.
- Registering a consumer to consume a single message is not optimal.
- `Consumers` are typically registered during application startup.
- They often would live as long as their connection or even application runs.
- `Applications` can subscribe to have RabbitMQ push enqueued messages (deliveries) to them.
    - This is done by registering a consumer (subscription) on a queue.
- When registering a consumer applications can choose one of two delivery modes:
    - `Automatic` (deliveries require no acknowledgement, a.k.a. "fire and forget").
    - `Manual` (deliveries require client acknowledgement).
- Single active consumer allows to have only one consumer at a time.
    - Consuming with only one consumer is useful when messages must be consumed 
    and processed in the same order they arrive in the queue.

### Queues

- A `queue` in RabbitMQ is an ordered collection of `messages`. 
- `Messages` are enqueued and dequeued (delivered to consumers) in a FIFO manner.
- `Queues` have names so that applications can reference them.
- `Queue` names starting with "amq." are reserved.
- `Queues` can be durable or transient.

### Channels

- `Applications` open a channel right after successfully opening a connection.
- Much like `connections`, `channels` are meant to be long lived.
- When a channel's connection is closed, so is the channel.

## Hello World!

- A `producer` (sender) that sends a single message.
    - Producer `sends` messages to the "hello" queue.
    - Producing means nothing more than sending.
    - Many producers can send messages that go to one queue
- A `consumer` (receiver) that receives messages and prints them out.
    - Consumer `receives` messages from the "hello" queue.
    - Consuming has a similar meaning to receiving.
    - A consumer is a program that mostly waits to receive messages.
    - Many consumers can try to receive data from one queue.
- A `queue` is the name for the post box in RabbitMQ. 
- A `producer` (sender) that sends messages.
- A `consumer` (receiver) that receives messages and prints them out.
- Before sending we need to make sure the recipient queue exist.
- In `RabbitMQ` a message can never be sent directly to the `queue`, it always needs to go through an `exchange`.
    - To use a `default exchange` identified by an empty string.
- The `queue` name needs to be specified in the `routing_key` parameter.
- Before exiting the program we need to make sure the network buffers were flushed and our message was actually delivered to RabbitMQ.
    - We can do it by gently closing the connection.
- `queue_declare` is idempotent, we can run the command as many times as we like, and only one will be created.
- Receiving messages from the `queue` is more complex.
    - It works by subscribing a `callback` function to a queue.
    - Whenever we receive a `message`, this callback function is called.
- First called the receive function to block and wait for messages.
    - The reciever should be running before the sender.
- Then called the send function to send a single message.
- Then the receiver will print the message.

## Work Queues

- Also known as `Task Queues`.
- Used to avoid doing a resource-intensive task immediately and having to wait for it to complete.
- A task is sent as a message and send it to the queue.
- A `worker` process running in the background will pop the tasks and eventually execute the job.
- When you run many workers the tasks will be shared between them.
- One of the advantages of using a `Task Queue` is the ability to easily `parallelise` work.
- By `default`, `RabbitMQ` will send each message to the next consumer, in `sequence`.
    - On average every consumer will get the same number of messages.
    - This way of distributing messages is called round-robin
- By `default` once `RabbitMQ` delivers message to the `consumer`, it immediately marks it for `deletion`.
    - In this case, if you terminate a worker, the message it was just processing is lost. 
    - In order to make sure a message is never lost, RabbitMQ supports message acknowledgments.
- If a `consumer` dies without sending an ack, RabbitMQ will understand that a message wasn't 
processed fully and will re-queue it.
- A `timeout` (30 minutes by default) is enforced on consumer delivery `acknowledgement`.
- `Manual` message `acknowledgments` are turned on by default.
    - It can be turned off via the `auto_ack` parameter.
- `Acknowledgement` must be sent on the same channel that received the delivery. 
    - ` ch.basic_ack(delivery_tag=method.delivery_tag)`.
- When `RabbitMQ` quits or crashes it will forget the queues and messages unless you tell it not to.
- To make sure that messages aren't lost we need to mark both the queue and messages as durable.
    - `channel.queue_declare(queue='hello', durable=True)`.
- To mark our `messages` as `persistent`:
    - Supply a `delivery_mode` property with the value of `pika.DeliveryMode.Persistent`.
- `RabbitMQ` doesn't know anything about that and will still dispatch messages evenly.
    - `RabbitMQ` just dispatches a message when the message enters the queue.
    - The `Channel#basic_qos` channel method with the `prefetch_count=1` setting tell RabbitMQ not 
    to give more than one message to a worker at a time.

## Publish/Subscribe

- This `pattern` delivers a message to `multiple` consumers.
- Every running copy of the receiver program will get the messages.
- A `producer` is a user application that sends messages.
- A `queue` is a buffer that stores messages.
- A `consumer` is a user application that receives messages.
- The core idea in the messaging model in `RabbitMQ` is that the `producer` never sends any messages directly to a `queue`.
- Instead, the `producer` can only send messages to an `exchange`.
- An `exchange` is a very simple thing:
    - On one side it receives messages from producers.
    - On the other side it pushes them to queues.
    - The exchange must know exactly what to do with a message it receives.
    - The rules for that are defined by the exchange type.
- There are a few exchange `types` available: 
    - `Direct`: delivers messages to queues based on the message routing key.
    - `Topic`: routes messages to one or many queues based on matching between a message routing key.
    - `Headers`: routing on multiple attributes that are more easily expressed as message headers than a routing key.
    - `Fanout`: broadcasts all the messages it receives to all the queues it knows. 
- To `create` a `queue` with a random name, supply empty queue parameter to `queue_declare`.
- To `remove` a `queue` when the consumer connection is closed, use the `exclusive` parameter.
- That `relationship` between `exchange` and a `queue` is called a `binding`.

## Routing

## Topics

## RPC

## Publisher Confirms

