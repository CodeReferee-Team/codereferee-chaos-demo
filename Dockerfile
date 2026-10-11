FROM python:3.12-slim
WORKDIR /app
COPY . .
# 두 포트 노출 -> 진입 포트가 모호 -> resolve_plan이 ConfigurationRequired.
# 배포 프로필 또는 .codereferee/validation.yaml의 port로 해소한다(탈출구).
EXPOSE 8000
EXPOSE 9000
CMD ["python", "app.py"]
