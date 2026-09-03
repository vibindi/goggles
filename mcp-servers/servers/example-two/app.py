"""Placeholder MCP server #2.

One of possibly many MCP servers hosted by this container — see
mcp-servers/entrypoint.py and mcp-servers/servers.json. SERVICE_NAME and PORT
are injected by the supervisor. Replace this with a real MCP server
implementation when ready; the file layout (one directory per server under
servers/) stays the same.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE_NAME = os.environ.get("SERVICE_NAME", "example-two")
PORT = int(os.environ.get("PORT", "8002"))


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
