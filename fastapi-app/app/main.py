"""FastAPI application entry point."""
from fastapi import FastAPI

from .routers import auth, flights

app = FastAPI()
app.include_router(auth.router)
app.include_router(flights.router)


@app.get("/")
async def root() -> dict:
    """Return a simple welcome message."""
    return {"message": "Hello World"}
