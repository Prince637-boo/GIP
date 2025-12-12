# Service d'Authentification

Ce service est responsable de la gestion des identités des utilisateurs, de l'authentification et du contrôle d'accès basé sur les rôles (RBAC) au sein de la plateforme AeroCast.

## Fonctionnalités

- Inscription de nouveaux utilisateurs.
- Connexion des utilisateurs via email et mot de passe.
- Génération de JSON Web Tokens (JWT) pour les sessions authentifiées.
- Protection des routes basée sur les rôles (`ADMIN`, `COMPAGNIE`, `ATC`, `PASSAGER`).
- Gestion des entités `User` et `Company`.

## Endpoints API

- `POST /auth/register`: Crée un nouvel utilisateur.
- `POST /auth/login`: Authentifie un utilisateur et retourne un `access_token`.
- `GET /users/me`: Récupère les informations de l'utilisateur actuellement connecté.

Pour une liste complète des endpoints, veuillez consulter la documentation OpenAPI auto-générée sur `/docs` lorsque le service est en cours d'exécution.

## Variables d'environnement

Ce service nécessite les variables suivantes dans le fichier `.env` :

- `SECRET_KEY`: Une chaîne secrète pour signer les JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: La durée de validité du token d'accès.
- `DATABASE_URL`: L'URL de connexion à la base de données PostgreSQL.

## Lancer les tests

Pour exécuter les tests spécifiques à ce service :

```bash
pytest tests/auth/
```
