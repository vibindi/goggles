"""Supervisor for the mcp-servers container.

This one Docker Compose service hosts multiple MCP servers as separate
processes. Every entry in servers.json gets launched from
servers/<name>/app.py with PORT and SERVICE_NAME set in its environment.

To add a server: create servers/<name>/app.py and add a "<name>": <port>
entry to servers.json (port must fall inside the range this service exposes
in docker-compose.yml, default 8001-8010). No Dockerfile or compose changes
needed as long as it fits that range.
"""

import json
import os
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "servers.json")

procs = {}


def shutdown(*_):
    print("[supervisor] shutting down")
    for p in procs.values():
        p.terminate()
    for p in procs.values():
        p.wait()
    sys.exit(0)


def main():
    with open(MANIFEST) as f:
        manifest = json.load(f)

    if not manifest:
        print("[supervisor] servers.json is empty, nothing to run", file=sys.stderr)
        sys.exit(1)

    for name, port in manifest.items():
        script = os.path.join(HERE, "servers", name, "app.py")
        env = {**os.environ, "PORT": str(port), "SERVICE_NAME": name}
        print(f"[supervisor] starting {name} on :{port}")
        procs[name] = subprocess.Popen([sys.executable, script], env=env)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # A single crashed server should bring the whole container down rather
    # than run silently short, so compose/health checks surface the failure.
    while True:
        for name, p in procs.items():
            if p.poll() is not None:
                print(f"[supervisor] {name} exited (code {p.returncode}); stopping the rest")
                shutdown()
        time.sleep(1)


if __name__ == "__main__":
    main()
