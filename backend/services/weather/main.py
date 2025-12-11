from fastapi import FastAPI
from services.weather.routes.weather_routes import router as weather_router

app = FastAPI(title="Weather Service")


app.include_router(weather_router)
