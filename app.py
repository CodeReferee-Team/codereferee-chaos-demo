import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# 두 포트를 여는 서비스를 흉내낸다(API 8000, 메트릭 9000). 어느 쪽이 트래픽
# 진입점인지 Dockerfile만으로는 알 수 없다 -> 샌박이 배포 플랜을 못 정함.
# (이 코드는 실제로 배포되지 않는다. resolve_plan 단계에서 ConfigurationRequired로 멈춘다.)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"status": "ok"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
