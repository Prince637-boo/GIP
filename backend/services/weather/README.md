# Service d'Orientation Passagers

Ce service fournit aux passagers des instructions optimales pour se déplacer dans l’aéroport en fonction de la météo, de l’état du vol et du suivi des bagages. Les instructions sont calculées en temps réel pour minimiser les retards et assurer une expérience fluide.

## Architecture

Le service s’appuie sur un moteur de décision (DecisionEngine) qui agrège plusieurs sources de données pour générer des instructions personnalisées :

- Données météo : via `MeteoServiceClient`
- Statut des bagages : via `BagageServiceClient`
- Informations vol : via `VolServiceClient`
- Décision et instructions : le DecisionEngine combine les données pour produire :
  - instructions détaillées (sécurité, zone d’attente, embarquement),
  - alertes (changement de porte, météo critique, urgence temporelle),
  - parcours optimal JITB (Just In Time Boarding).

## Endpoints

### Obtenir l'orientation (GET)
GET `/api/orientation/{numero_vol}/{id_bagage}?position_estimee=<position>`

Paramètres :
- `numero_vol` : numéro du vol (ex. `AF1234`)
- `id_bagage` : identifiant du bagage
- `position_estimee` (optionnel) : position actuelle du passager

Réponse : `OrientationResponse`  
Contient : situation actuelle, instructions détaillées, alertes, parcours recommandé.

Exemple d’appel :
```
GET /api/orientation/AF1234/BAG123?position_estimee=zone_embarquement
```

### Obtenir l'orientation (POST)
POST `/api/orientation/`

Payload JSON :
```json
{
  "numero_vol": "AF1234",
  "id_bagage": "BAG123",
  "position_estimee": "zone_embarquement"
}
```

Réponse : `OrientationResponse` (mêmes champs que GET)

### Vérification de santé
GET `/api/orientation/health`

Réponse exemple :
```json
{
  "status": "healthy",
  "service": "orientation-service",
  "timestamp": "2025-12-11T07:00:00Z"
}
```

## Fonctionnalités principales

- Calcul en temps réel de l’orientation d’un passager dans l’aéroport.
- Génération automatique d’instructions et d’alertes selon le contexte :
  - problème de bagage,
  - changement de porte,
  - conditions météo critiques,
  - temps restant avant embarquement.
- Couplage avec les services de bagages, météo et vols pour un écosystème complet.
- Logging des orientations calculées pour suivi et amélioration du DecisionEngine.

## Dépendances

- FastAPI
- SQLAlchemy (si intégration base de données pour logs)

Services externes :
- `MeteoServiceClient`
- `BagageServiceClient`
- `VolServiceClient`  
  - Méthodes courantes : `get_flight_status(numero_vol)`, `get_gate(numero_vol)`, `subscribe_updates(numero_vol)`
  - Configuration : clé API via `VOL_SERVICE_API_KEY`, endpoint configurable via `VOL_SERVICE_URL`
  - Tests : fournir un mock (`MockVolServiceClient`) ou une fixture pytest pour isoler le DecisionEngine

## Lancer les tests

Pour exécuter les tests :
```
poetry run pytest tests/orientation/
```

## Notes

Le DecisionEngine est modulaire et extensible : ajouter des règles, priorisations et métriques améliore l’optimisation du parcours passager. Les instructions incluent le temps estimé pour chaque action et sont priorisées selon criticité et délai.
