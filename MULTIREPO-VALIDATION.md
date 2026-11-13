# 멀티레포 운영 검증 브랜치

이 브랜치는 기존 단일 서비스 데모를 확장한 version 3 검증 입력이다.
gateway는 이 레포에서, API는 고정 SHA의 공개 FastAPI 예제 레포에서 clone·빌드한다.

`/api/items/1` 업무 probe가 gateway와 API를 모두 거친다.
Sandbox의 `repositoryPatches.upstream`으로 API 응답과 테스트를 변경하고,
누적 패치를 유지한 채 기준 레포의 probe 기대값을 변경해 그룹 전체를 재검증한다.
이 문서 자체는 실행 성공 기록이 아니며 실제 결과는 운영 검증 완료 후 별도로 기록한다.
