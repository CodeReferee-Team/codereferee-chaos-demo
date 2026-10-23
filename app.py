"""Redis 장애 뒤 복구하지 못하는 fixture.

캐시 호출이 한 번 실패하면 차단기를 열고, 다시 닫는 경로가 없다. 장애가 걷힌 뒤에도
/api/session은 계속 503을 낸다. dependency_redis_outage에서 recovered=false로 Fail이
나야 하고, 일정 시간 뒤 다시 시도하도록 고치면 Pass가 나야 한다.

/health는 Redis를 보지 않는다. 기동 판정과 업무 판정을 분리해야 이 결함이 "기동 실패"가
아니라 "장애 후 미복구"로 관측된다.
"""
import os

import redis
from redis.backoff import NoBackoff
from redis.retry import Retry
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# redis-py 6 이상은 기본으로 타임아웃을 10번까지 재시도해서 한 호출이 20초 넘게 버틴다.
# 15초짜리 장애가 그 안에 걷히면 예외가 나지 않아 결함이 드러나지 않는다(2026-10-23 실서버).
# 재시도를 끄고 2초 만에 실패하게 해서 차단기가 실제로 열리게 한다.
cache = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']),
                    socket_timeout=2, socket_connect_timeout=2, retry=Retry(NoBackoff(), 0))

# 캐시가 한 번 실패하면 더 이상 부르지 않는다.
cache_broken = False


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/session")
def session():
    global cache_broken
    if cache_broken:
        return JSONResponse({"error": "cache unavailable"}, status_code=503)
    try:
        cache.set("session:probe", "ok", ex=30)
        return {"session": cache.get("session:probe").decode()}
    except redis.RedisError:
        cache_broken = True
        return JSONResponse({"error": "cache unavailable"}, status_code=503)
