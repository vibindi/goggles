FROM python:3.12-slim

WORKDIR /app
COPY entrypoint.py healthcheck.py servers.json ./
COPY servers/ ./servers/

ENV PYTHONUNBUFFERED=1
EXPOSE 8001-8010

CMD ["python", "entrypoint.py"]
