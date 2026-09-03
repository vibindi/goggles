FROM python:3.12-slim

WORKDIR /app
COPY app.py .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

CMD ["python", "app.py"]
