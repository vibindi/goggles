# goggles

A multi-service application orchestrated with Docker Compose. Each service lives in its
own top-level directory and joins a shared `goggles-network` so they can reach each other
by service name.

## Layout

```
goggles/
├── docker-compose.yml   # orchestrates all services
├── Makefile              # wraps common docker compose commands
├── .env.example           # copy to .env, override ports etc.
├── backend/               # placeholder service — replace with the real backend
├── mcp-servers/            # one container hosting multiple MCP servers
│   ├── entrypoint.py         # supervisor: launches every server in servers.json
│   ├── healthcheck.py         # checks every server's /health
│   ├── servers.json            # server name -> port manifest
│   └── servers/
│       ├── example-one/          # placeholder MCP server
│       └── example-two/           # placeholder MCP server
├── ollama/                 # notes for the official ollama/ollama image
└── langfuse/                # not wired up yet — see langfuse/README.md
```

`backend/` and each server under `mcp-servers/servers/` currently run minimal stub HTTP
servers (stdlib-only, one `/health` endpoint) whose only job is to prove the Compose
wiring — build, network, ports, healthchecks — works end-to-end. Replace their contents
wholesale once real implementation work starts.

## Adding a new service

1. Create a new top-level directory (e.g. `some-new-service/`) with its own `Dockerfile`.
2. Add a service block to `docker-compose.yml` on the `goggles-network`.
3. Add any ports/secrets it needs to `.env.example`.

## Adding a new MCP server

MCP servers are lightweight, so `mcp-servers/` runs several of them as separate processes
in one container rather than one container each:

1. Create `mcp-servers/servers/<name>/app.py`.
2. Add a `"<name>": <port>` entry to `mcp-servers/servers.json`, using a free port inside
   the range `docker-compose.yml` maps for this service (default `8001-8010`).

No Dockerfile or compose changes needed unless you exceed that port range — bump
`MCP_SERVERS_PORT_RANGE` in `.env` if you do. If a particular MCP server needs real
isolation (its own base image, independent scaling/restarts), pull it out into its own
top-level directory and compose service instead, following the `backend/` pattern.

## Running

```bash
cp .env.example .env
make up      # build + start everything, detached
make logs    # follow logs (make logs s=backend for one service)
make ps      # see what's running
make down    # stop everything
make clean   # stop everything and remove volumes (e.g. pulled ollama models)
```

Once running:
- Backend health: `curl localhost:8000/health`
- MCP servers health: `curl localhost:8001/health`, `curl localhost:8002/health`, ...
- Ollama API: `curl localhost:11434` (see `ollama/README.md` for pulling a model)

Langfuse isn't included yet — see `langfuse/README.md` for why and how to add it.
