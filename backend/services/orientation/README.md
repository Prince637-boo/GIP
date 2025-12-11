# Service d’Orientation Passagers

Ce service fournit des instructions personnalisées et des alertes aux passagers pour optimiser leurs déplacements dans l’aéroport, en tenant compte de la météo, du statut des bagages et des informations sur le vol. Il est conçu pour être consommé par des applications front-end ou mobiles pour guider les passagers en temps réel.

## Architecture

Le service repose sur plusieurs composants :

- **Client Vol** (`VolServiceClient`) : récupère les informations du vol (porte actuelle, horaires, terminal…).
- **Client Bagage** (`BagageServiceClient`) : récupère le statut et la position du bagage.
- **Client Météo** (`MeteoServiceClient`) : récupère les conditions météo et leur impact potentiel.
- **Decision Engine** (`DecisionEngine`) : moteur de décision qui analyse la situation et génère les instructions et alertes.
- **Logging en arrière-plan** (optionnel) : conserve un historique des orientations calculées.

Le service transforme ces données en instructions détaillées, alertes et parcours optimisés pour le passager.

## Endpoints API

### 1. Obtenir l’orientation (GET)
`GET /api/orientation/{numero_vol}/{id_bagage}?position_estimee=<position>`

Paramètres :
- `numero_vol` : numéro du vol (ex: `AF1234`)
- `id_bagage` : identifiant du bagage
- `position_estimee` (optionnel) : position actuelle du passager dans l’aéroport

Réponse (exemple de structure) :
```json
{
    "success": true,
    "numero_vol": "AF1234",
    "timestamp": "2025-12-11T07:00:00Z",
    "situation": "embarquement_possible",
    "instructions": [ /* ... */ ],
    "alertes": [ /* ... */ ],
    "parcours": [ /* ... */ ]
}
```

### 2. Obtenir l’orientation (POST)
`POST /api/orientation/`

Body (JSON) :
```json
{
    "numero_vol": "AF1234",
    "id_bagage": "BAG00123",
    "position_estimee": "zone_embarquement"
}
```

Réponse : identique au GET.

### 3. Vérification de santé
`GET /api/orientation/health`

Réponse (exemple) :
```json
{
    "status": "healthy",
    "service": "orientation-service",
    "timestamp": "2025-12-11T07:00:00Z"
}
```

## Flux de traitement

1. Le service reçoit le `numero_vol` et l’`id_bagage`.
2. Les clients `VolServiceClient`, `BagageServiceClient` et `MeteoServiceClient` récupèrent les données nécessaires.
3. `DecisionEngine` analyse la situation du passager et calcule :
     - les instructions prioritaires (ex. : passer la sécurité, se rendre à la porte),
     - les alertes contextuelles,
     - le parcours optimisé avec estimations temporelles.
4. Les résultats sont renvoyés au client et peuvent être loggés en arrière-plan.

### Exemple de sortie du DecisionEngine (format attendu)

Exemple de réponse renvoyée par l'API :
```json
{
    "success": true,
    "numero_vol": "AF1234",
    "timestamp": "2025-12-11T07:00:00Z",
    "situation": "embarquement_possible",
    "instructions": [
        { "id": "inst-1", "type": "securite", "message": "Passer le contrôle de sécurité avant 08:15", "priorite": 1 },
        { "id": "inst-2", "type": "porte", "message": "Se rendre à la porte A12", "priorite": 2 }
    ],
    "alertes": [
        { "id": "al-1", "niveau": "warning", "message": "Vent fort attendu : prévoir délais pour navette de terminal" }
    ],
    "parcours": [
        { "etape": 1, "action": "prendre_navette", "depuis": "zone_arrivee", "vers": "terminal_A", "duree_estimee_min": 10 },
        { "etape": 2, "action": "suivre_signalisation", "depuis": "terminal_A", "vers": "porte_A12", "duree_estimee_min": 5 }
    ]
}
```

## Remarques rapides

- `instructions` : triées par le champ `priorite` (1 = plus urgente).
- `alertes` : champ `niveau` = `info` | `warning` | `critical` ; inclure durée ou condition si pertinent.
- `parcours` : liste d'étapes séquentielles avec durée estimée en minutes.
- Horodatage : UTC ISO 8601.
- Logging : optionnel, conserver les entrées pour audit et analyse des décisions.

## Comportement attendu du DecisionEngine

- Fusionner les données Vol, Bagage et Météo pour définir la `situation`.
- Générer des instructions prioritaires et alertes contextuelles exploitables par un front-end.
- Fournir un parcours optimisé et des estimations temporelles ; recommander des actions alternatives si la situation est critique.
- Être idempotent pour des requêtes identiques reçues dans un court délai (retourner les mêmes instructions / alertes).
- Exposer un niveau de journalisation configurable (`debug` / `info` / `error`) pour faciliter les tests et la production.

## Parcours optimisé jusqu’à la porte

Les instructions et alertes sont renvoyées au client et peuvent être loggées en arrière-plan pour suivi. Le parcours doit décomposer en étapes claires avec durées estimées et actions recommandées.

## Lancer les tests

Pour tester le service d’orientation :
```bash
poetry run pytest tests/orientation/
```

Ces tests vérifient la génération d’instructions et d’alertes en fonction de scénarios simulés (vol, bagage, météo).

## Notes

- Les instructions sont priorisées selon l’urgence et le type d’action.
- Les alertes et instructions peuvent être directement affichées sur une application mobile ou un terminal d’information.
- Le service ne gère pas directement les données des bagages ou vols ; il dépend des services externes pour ces informations.
