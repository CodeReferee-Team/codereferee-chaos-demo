# chaos-demo

복원력 데모용 작은 FastAPI 서비스. 기동이 느려(READY_DELAY초) 단일 replica가
종료되면 그 시간만큼 서비스가 중단된다. CodeReferee 카오스(container_kill)가 이
약점을 드러내고, Refiner가 `.codereferee/validation.yaml`의 replicas를 늘려 고친다.
