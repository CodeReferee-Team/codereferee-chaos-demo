"""의존성 장애 시나리오용 fixture. Postgres와 Redis를 각각 업무 API 하나로 노출한다.

/health는 의존성을 보지 않는다. 기동 판정과 업무 판정을 분리해야 의존성 장애가
"기동 실패"가 아니라 "업무 API 실패"로 관측되기 때문이다.
"""
import os

import psycopg
import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

DB_DSN = (f"host={os.environ['DB_HOST']} port={os.environ['DB_PORT']} dbname={os.environ['DB_NAME']} "
          f"user={os.environ['DB_USER']} password={os.environ['DB_PASSWORD']} connect_timeout=2")
cache = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']),
                    socket_timeout=2, socket_connect_timeout=2)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/orders")
def orders():
    try:
        with psycopg.connect(DB_DSN) as conn:
            count = conn.execute("SELECT 1").fetchone()[0]
        return {"orders": count}
    except psycopg.Error:
        return JSONResponse({"error": "database unavailable"}, status_code=503)


@app.get("/api/session")
def session():
    try:
        cache.set("session:probe", "ok", ex=30)
        return {"session": cache.get("session:probe").decode()}
    except redis.RedisError:
        return JSONResponse({"error": "cache unavailable"}, status_code=503)
