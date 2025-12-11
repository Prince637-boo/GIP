# Service de Suivi des Bagages

Ce service assure le suivi en temps réel des bagages grâce à plusieurs sources d’événements :

- Scan QR Code (agents)

- Mise à jour de statut

- Trackers GPS (appareils IoT physiques)

- GPS manuel (via app mobile ou outil interne)

Il combine FastAPI, WebSockets et Redis (Pub/Sub) pour offrir une diffusion instantanée aux applications clientes.

## Architecture

Le service repose sur une architecture asynchrone et événementielle, entièrement découplée :

1.  **Publication d'Événements :** 

Divers composants du système publient des messages sur des canaux Redis :

- Scan QR Code → baggage.scan

- Changement de statut → baggage.status

- Mises à jour GPS

    - via tracker IoT → baggage.gps

    - via application mobile → baggage.gps


2.  **Abonnement et Diffusion :** 

Le serveur WebSocket :

- s'abonne aux canaux Redis : baggage.scan, baggage.status, baggage.gps

- transmet chaque événement dès qu'il est reçu

- envoie les données JSON au client en temps réel

3.  **Client WebSocket :** 

Le client (React, Flutter, interface admin, etc.) reçoit les événements immédiatement pour :

- mettre à jour la position GPS sur la carte

- afficher les scans en temps réel

- afficher les statuts mis à jour

- notifier les opérateurs

## Endpoint WebSocket

- `ws://<host>/ws/baggages/stream`: 

Ce flux envoie tous les événements liés aux bagages, y compris :

- Scans QR Code

- Changements de statut

- Mises à jour GPS (trackers IoT + scan manuel)

## Endpoints API liés au GPS

1. **Mise à jour GPS classique (app mobile, agent)**

```bash
POST /baggages/update-location
```


Met à jour la latitude / longitude d’un bagage et publie sur Redis baggage.gps.

2. **Ingestion des trackers GPS IoT**

```bash
POST /trackers/ingest
```

Route appelée par un appareil GPS physique attaché au bagage.
Elle :

1. reçoit { device_id, lat, lon }

2. retrouve le bagage associé

3. met à jour la position GPS

4. publie sur Redis (baggage.gps)

5. déclenche une mise à jour instantanée dans le WebSocket

## Canaux Redis

Le service s'abonne aux canaux Redis suivants :

baggage.scan
Scans QR Code (agents, bornes, app)

- baggage.status
Changements de statut opérationnels

- baggage.gps
Toutes sources GPS : tracker IoT + app mobile + mise à jour manuelle

Ces canaux permettent une architecture totalement temps réel et découplée.

## Fonctionnalités couvertes

- Suivi GPS continu

- Détection des scans QR

- Gestion des statuts de bagages

- Ingestion des données IoT

- Diffusion en temps réel pour dashboards & applications mobiles

- Compatibilité avec les systèmes aéronautiques (Ops/Bagages)

## Lancer les tests

Des tests automatisés vérifient :

- la publication Redis

- l’écoute des canaux Redis

- la diffusion WebSocket

- la cohérence du flux temps réel

Pour exécuter uniquement les tests liés au suivi des bagages :

```bash
pytest tests/baggages/
```
