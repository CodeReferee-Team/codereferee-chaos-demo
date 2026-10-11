from fastapi import FastAPI

app = FastAPI()


def compute_quota(plan: dict) -> int:
    # BUG: assumes the "limit" key always exists. Free plans omit it,
    # so the "/quota" handler raises KeyError at request time -> HTTP 500.
    return plan["limit"] * 2


@app.get("/")
def root():
    # 건강한 루트. readiness/startup probe(healthPath 기본 "/")가 여기를 쳐서 통과한다.
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/quota")
def quota():
    # 결함은 probe가 치지 않는 이 엔드포인트에만 있다. 샌박 business probe는
    # healthPath(기본 "/")로 고정이라 /quota를 절대 호출하지 않는다 -> 미탐지.
    plan = {"name": "free"}  # no "limit" key
    return {"quota": compute_quota(plan)}
