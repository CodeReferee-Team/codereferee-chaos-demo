from fastapi import FastAPI

app = FastAPI()


def compute_quota(plan: dict) -> int:
    # 결함 2: "limit" 키가 항상 있다고 가정. free plan은 생략 -> /quota가 KeyError -> HTTP 500.
    return plan["limit"] * 2


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    # healthPath(validation.yaml) = /health. readiness/business probe 둘 다 여기만 친다.
    return {"status": "healthy"}


@app.get("/quota")
def quota():
    # 결함은 probe 밖(/quota)에만. 결함 1(single replica 토폴로지)과 공존하지만
    # 샌박 evidence에는 토폴로지 신호만 뜨고 이 코드버그는 안 보인다.
    plan = {"name": "free"}  # no "limit" key
    return {"quota": compute_quota(plan)}
