from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "ok"}
