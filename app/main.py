"""작은 HTTP 서비스. 복원력 데모용 — 기동이 느려서(READY_DELAY) 단일 replica가
죽으면 그 시간만큼 전면 중단된다. replica를 늘리면 다른 파드가 그 틈을 메운다."""
import os, threading, time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
_ready = False
READY_DELAY = int(os.getenv("READY_DELAY", "35"))  # 기동 지연(초)

def _warmup():
    global _ready
    time.sleep(READY_DELAY)
    _ready = True

threading.Thread(target=_warmup, daemon=True).start()

@app.get("/")
def root():
    # 준비 전이면 503 — 단일 replica가 재기동되는 동안 요청이 실패한다.
    if not _ready:
        return JSONResponse({"status": "starting"}, status_code=503)
    return {"status": "ok"}

@app.get("/health")
def health():
    return JSONResponse({"ready": _ready}, status_code=200 if _ready else 503)
