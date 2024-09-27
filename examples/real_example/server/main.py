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
    emmit_event("list_users")
    return [user for user in users.values()]


@app.get("/api/v1/users/{name}")
def get_user(name: str) -> User:
    emmit_event("get_user", name)
    return users.get(name)


@app.post("/api/v1/users/{name}")
def add_user(name: str) -> User:
    user = User(name=name)
    users[name] = user
    emmit_event("add_user", name)
    return user


@app.delete("/api/v1/users/{name}")
def delete_user(name: str) -> User:
    user = users[name]
    del users[name]
    emmit_event("delete_user", name)
    return user


def emmit_event(event_name: str, name: str | None = None) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    payload = {"event": event_name}
    if name:
        payload.update({"name": name})

    channel.basic_publish(exchange="", routing_key="hello", body=json.dumps(payload))
    print(f" [x] Sent '{json.dumps(payload)}'")
    connection.close()
