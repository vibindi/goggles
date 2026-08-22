from fastapi import FastAPI

app = FastAPI(
    title="LangGraph Agent API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Agent API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
