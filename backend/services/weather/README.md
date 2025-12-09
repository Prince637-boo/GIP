# Service Météo

Ce service fournit des données météorologiques en temps réel pour des coordonnées géographiques spécifiques. Il agit comme un proxy intelligent, mettant en cache les données pour réduire la latence et limiter les appels à l'API externe.

## Fonctionnalités

- Récupération des données météo actuelles (température, vitesse du vent) à partir de l'API [Open-Meteo](https://open-meteo.com/).
- Mise en cache en base de données des résultats pour éviter les appels redondants.
- Validation des réponses de l'API externe à l'aide de schémas Pydantic.
- Une tâche de fond (worker Celery) qui met à jour périodiquement les données météo pour des lieux d'intérêt prédéfinis.

## Endpoint API

- `GET /weather/`: Récupère les données météo pour une latitude et une longitude données.
  - **Paramètres de requête :** `latitude` (float), `longitude` (float).
  - **Comportement :**
    1.  Vérifie d'abord si des données récentes existent dans la base de données.
    2.  Si ce n'est pas le cas, appelle l'API Open-Meteo.
    3.  Sauvegarde la nouvelle réponse dans la base de données avant de la retourner.

## Tâche de fond (Celery)

- **Tâche :** `services.weather.workers.tasks.fetch_and_save_weather`
- **Fréquence :** Exécutée toutes les heures (configurable).
- **Action :** Récupère et sauvegarde les données météo pour une liste de lieux définis dans `services/weather/config.py`.

## Variables d'environnement

- `DATABASE_URL`: L'URL de connexion à la base de données PostgreSQL.
- `WEATHER_API_URL`: L'URL de base de l'API Open-Meteo.
- `CELERY_BROKER_URL`: L'URL du broker de messages RabbitMQ.

## Lancer les tests

Pour exécuter les tests spécifiques à ce service :

```bash
poetry run pytest tests/weather/
```
