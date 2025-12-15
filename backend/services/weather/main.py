from fastapi import FastAPI
from services.weather.routers.weather import router as weather_router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="Weather Service",
    root_path="/api/weather",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

Instrumentator().instrument(app).expose(app)

app.include_router(weather_router)
