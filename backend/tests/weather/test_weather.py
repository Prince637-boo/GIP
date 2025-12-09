import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from services.weather.main import app
from services.weather.service_weather import create_weather_data
from services.weather.schemas.weather import WeatherCreate
from services.weather.schemas.open_meteo import OpenMeteoResponse
from libs.common.database import get_db
from services.weather.dependencies.weather_deps import get_open_meteo_service

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def client(db_session: AsyncSession):
    """Crée un client de test pour l'application Météo."""
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def mock_open_meteo_service():
    """Mock propre du service Open-Meteo (async)"""
    mock_service = MagicMock()
    mock_service.fetch_weather_from_api = AsyncMock(
        return_value=OpenMeteoResponse.model_validate({
            "latitude": 48.88,
            "longitude": 2.36,
            "current_weather": {
                "temperature": 15.0,
                "windspeed": 10.0,
                "weathercode": 3,
                "time": "2023-10-27T12:00"
            }
        })
    )
    return mock_service


async def test_get_weather_from_api_when_db_is_empty(
    client: AsyncClient,
    mock_open_meteo_service
):
    # Override de la dépendance
    app.dependency_overrides[get_open_meteo_service] = lambda: mock_open_meteo_service

    lat, lon = 48.88, 2.36
    response = await client.get(f"/weather/?latitude={lat}&longitude={lon}")

    data = response.json()
    assert response.status_code == 200

    assert data["latitude"] == lat
    assert data["longitude"] == lon
    assert data["temperature"] == 15.0
    assert data["wind_speed"] == 10.0

    app.dependency_overrides.clear()


async def test_get_weather_from_db_when_data_is_recent(
    client: AsyncClient,
    db_session: AsyncSession
):
    lat, lon = 51.50, -0.12

    weather_in_db = await create_weather_data(
        db_session,
        WeatherCreate(
            location_name="London",
            latitude=lat,
            longitude=lon,
            temperature=12.5,
            wind_speed=5.5
        )
    )

    response = await client.get(f"/weather/?latitude={lat}&longitude={lon}")

    data = response.json()
    assert response.status_code == 200

    assert data["id"] == weather_in_db.id
    assert data["temperature"] == 12.5
    assert data["location_name"] == "London"
