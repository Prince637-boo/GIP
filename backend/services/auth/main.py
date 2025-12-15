from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.auth import router as auth_router
from .middleware.logging import LoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Auth Service", version="1.0.0")

# Middlewares
app.add_middleware(LoggingMiddleware)

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # provisoire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
