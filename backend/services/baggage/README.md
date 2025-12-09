# Service de Suivi des Bagages

Ce service fournit un flux en temps réel des mises à jour de statut des bagages via une connexion WebSocket. Il est conçu pour diffuser des événements à mesure qu'ils se produisent dans le système de traitement des bagages.

## Architecture

Le service utilise une architecture Pub/Sub pour découpler la source des événements de la diffusion aux clients.

1.  **Publication d'Événements :** D'autres parties du système (non implémentées ici) publient des messages sur des canaux Redis spécifiques (par exemple, lorsqu'un bagage est scanné).
2.  **Abonnement et Diffusion :** Le serveur WebSocket s'abonne à ces canaux Redis.
3.  **Client WebSocket :** Lorsqu'un message est reçu de Redis, le serveur le transmet immédiatement à tous les clients connectés au WebSocket.

## Endpoint WebSocket

- `ws://<host>/ws/baggages/stream`: Établit une connexion WebSocket pour recevoir les mises à jour de statut des bagages.

## Canaux Redis

Le service écoute les messages publiés sur les canaux Redis suivants :

- `baggage.scan`: Pour les événements de scan de bagages.
- `baggage.status`: Pour les changements de statut généraux (par exemple, "en transit", "retardé").

## Lancer les tests

Pour exécuter les tests spécifiques à ce service, qui simulent la publication de messages Redis et vérifient leur réception via WebSocket :

```bash
poetry run pytest tests/baggages/
```
