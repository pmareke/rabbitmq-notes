import json

import pika
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str


users: dict[str, User] = {}


@app.get("/api/v1/users")
def get_users() -> list[User]:
    send("list_users")
    return [user for user in users.values()]


@app.get("/api/v1/users/{name}")
def get_user(name: str) -> User:
    send("get_user", name)
    return users.get(name)


@app.post("/api/v1/users/{name}")
def add_user(name: str) -> User:
    user = User(name=name)
    users[name] = user
    send("add_user", name)
    return user


@app.delete("/api/v1/users/{name}")
def delete_user(name: str) -> User:
    user = users[name]
    del users[name]
    send("delete_user", name)
    return user


def send(event_name: str, name: str | None = None) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    if name:
        payload = json.dumps({"event": event_name, "name": name})
    else:
        payload = json.dumps({"event": event_name})

    channel.basic_publish(exchange="", routing_key="hello", body=payload)
    print(f" [x] Sent '{payload}'")
    connection.close()
