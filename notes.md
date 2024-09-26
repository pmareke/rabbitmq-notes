# RabbitMQ

- One broker to queue them all
- RabbitMQ is a reliable and mature messaging and streaming broker.

## AMQP 0-9-1

- AMQP 0-9-1 (Advanced Message Queuing Protocol) is a messaging protocol.
- Messaging brokers receive messages from publishers and route them to consumers.
- The model has a notion of message acknowledgements, when a message is delivered to 
a consumer the consumer notifies the broker.
    - Publishers choose how to handle situations like this by publishing messages using certain parameters.

### Exchanges

- Messages are published to exchanges.
- Then the broker either deliver messages to consumers subscribed to queues, or 
consumers fetch/pull messages from queues on demand.
- Exchanges then distribute message copies to queues using rules called bindings.
- Exchanges are AMQP 0-9-1 entities where messages are sent to.
- Exchanges take a message and route it into zero or more queues.
- Rxchanges are declared with a number of attributes, the most important of which are:
    - Name.
    - Durability (exchanges survive broker restart).
    - Auto-delete (exchange is deleted when last queue is unbound from it).
    - Arguments (optional, used by plugins and broker-specific features).
- Exchanges can be durable or transient:
    - Durable exchanges survive broker restart.
    - Transient exchanges do not.
- The default exchange is a direct exchange with no name pre-declared by the broker.
    - Very useful for simple applications.
    - Every queue that is created is automatically bound to it with a routing key which is the same as the queue name.
- A direct exchange delivers messages to queues based on the message routing key.
    - It's ideal for the unicast routing of messages.
- A fanout exchange routes messages to all of the queues that are bound to it and the routing key is ignored.
- Topic exchanges route messages to one or many queues based on matching between a message routing key and the 
pattern that was used to bind a queue to an exchange.
    - They are commonly used for the multicast routing of messages.

### Queues

- They store messages that are consumed by applications.
- Queues have some properties:
    - Name.
    - Durable (the queue will survive a broker restart).
    - Exclusive (used by only one connection and the queue will be deleted when that connection closes).
    - Auto-delete (queue that has had at least one consumer is deleted when last consumer unsubscribes).
    - Arguments (optional; used by plugins and broker-specific features such as message TTL, queue length limit, etc).

### Bindings

- They are rules that exchanges use to route messages to queues.

### Consumers

- Applications have to indicate interest in consuming messages from a particular queue.
- Each consumer (subscription) has an identifier called a consumer tag.

### Message Acknowledgements

-  There are two acknowledgement modes:
    - After broker sends a message to an application (using either basic.deliver or basic.get-ok method).
    - After the application sends back an acknowledgement (using the basic.ack method).
- The former choice is called the automatic acknowledgement model, while the latter is 
called the explicit acknowledgement model.
- If a consumer dies without sending an acknowledgement, the broker will redeliver it to another consumer.

### Message Attributes and Payload

- Messages in the AMQP 0-9-1 model have attributes:
    - Content type.
    - Content encoding.
    - Routing key.
    - Delivery mode (persistent or not).
    - Message priority.
    - Message publishing timestamp.
    - Expiration period.
    - Publisher application id.

## Hello World!

- A producer (sender) that sends a single message.
    - Producer sends messages to the "hello" queue.
- A consumer (receiver) that receives messages and prints them out.
    - Consumer receives messages from the "hello" queue.

## Work Queues

## Publish/Subscribe

## Routing

## Topics

## RPC

## Publisher Confirms

