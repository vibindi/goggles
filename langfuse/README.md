# Langfuse (placeholder)

Not wired up yet. Self-hosted Langfuse needs several coordinated containers
(Postgres, ClickHouse, Redis, MinIO/S3-compatible blob storage, plus the
`langfuse-web` and `langfuse-worker` images) — getting that combination right
is a real service-configuration task, not scaffolding, so it's deliberately
left out of `docker-compose.yml` for now (see the commented block there).

When it's time to add it for real, start from Langfuse's own self-hosting
docker-compose reference rather than reinventing it:
<https://langfuse.com/self-hosting/docker-compose>

## To wire it in later

1. Copy the relevant services (Postgres, ClickHouse, Redis, MinIO, `langfuse-web`,
   `langfuse-worker`) from the reference compose file into `docker-compose.yml`,
   or `include:` a dedicated `langfuse/docker-compose.yml` from the root file.
2. Add the required secrets/env vars (`DATABASE_URL`, `NEXTAUTH_SECRET`,
   `SALT`, `ENCRYPTION_KEY`, etc.) to `.env.example` and `.env`.
3. Join the `goggles-network` so `backend`/`mcp-servers` can reach it by
   service name for tracing.
