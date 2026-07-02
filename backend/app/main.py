from fastapi import FastAPI
from app.api.v4 import auth, cognition, telemetry, bus_stream
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="Aetherium Manifest API",
        version="4.0.0",
    )

    app.include_router(auth.router, prefix="/v4/auth", tags=["auth"])
    app.include_router(cognition.router, prefix="/v4/cognition", tags=["cognition"])
    app.include_router(telemetry.router, prefix="/v4/telemetry", tags=["telemetry"])
    app.include_router(bus_stream.router, prefix="/v4/bus", tags=["bus"])

    return app

app = create_app()
