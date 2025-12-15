from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.auth import router as auth_router
from .middleware.logging import LoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Auth Service",
    root_path="/api/auth",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


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
