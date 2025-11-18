from fastapi import FastAPI

from app.api.routes import health, users

app = FastAPI(title="Python Backend Project", version="0.3.0")

# Define the health enpoint routing
app.include_router(health.router, tags=["Health"])

# Define the users endpoint routing
app.include_router(users.router, tags=["Users"], prefix="/users")
