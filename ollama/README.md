# Ollama

Runs from the official [`ollama/ollama`](https://hub.docker.com/r/ollama/ollama) image
(see the `ollama` service in the root `docker-compose.yml`) — no custom Dockerfile needed
here.

- Model data persists in the `ollama-data` named volume, mounted at `/root/.ollama`.
- API is exposed on `${OLLAMA_PORT}` (default `11434`).

## Pulling a model

Once the stack is up (`make up`), pull a model into the running container:

```bash
docker compose exec ollama ollama pull llama3.2
```

Then call it:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?"
}'
```
