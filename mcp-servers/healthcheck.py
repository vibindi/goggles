"""Docker healthcheck for the mcp-servers container: every server listed in
servers.json must respond on its /health endpoint."""

import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "servers.json")) as f:
    manifest = json.load(f)

for name, port in manifest.items():
    try:
        urllib.request.urlopen(f"http://localhost:{port}/health", timeout=2)
    except Exception as e:
        print(f"{name} on :{port} failed: {e}", file=sys.stderr)
        sys.exit(1)

sys.exit(0)
