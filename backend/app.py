"""Placeholder backend service.

Stands in for the real backend so the Docker Compose scaffolding can be built,
wired to the shared network, and health-checked end-to-end before any real
application code exists. Replace this file (and the Dockerfile if needed)
once real implementation work starts.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE_NAME = "backend"
PORT = int(os.environ.get("PORT", "8000"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({"status": "ok", "service": SERVICE_NAME}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(f"[{SERVICE_NAME}] {fmt % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[{SERVICE_NAME}] listening on :{PORT}")
    server.serve_forever()
