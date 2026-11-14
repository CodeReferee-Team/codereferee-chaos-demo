import os

import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()
client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    socket_connect_timeout=1,
    socket_timeout=1,
)
dependency_failed = False


def read_item(item_id: int):
    global dependency_failed
    if dependency_failed:
        raise HTTPException(status_code=503, detail="Dependency circuit is open")
    try:
        client.ping()
    except redis.RedisError:
        dependency_failed = True
        raise HTTPException(status_code=503, detail="Redis is unavailable")
    return {"item_id": item_id}


@app.get("/")
def root():
    return read_item(1)


@app.get("/items/{item_id}")
def item(item_id: int):
    return read_item(item_id)


@app.get("/health")
def health():
    return {"status": "healthy"}
