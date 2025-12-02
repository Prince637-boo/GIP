✈️ Projet Stratégique ANAC : Sécurité, Efficacité et Expérience PassagerBienvenue dans le dépôt GitHub du Projet Stratégique pour l'Aviation Civile au Togo, développé en collaboration avec l'ANAC (Agence Nationale de l'Aviation Civile).Ce projet vise à moderniser les opérations aéronautiques en intégrant deux piliers technologiques majeurs :L'Intelligence Artificielle (IA) pour la Météo : Prévision ultra-précise des phénomènes dangereux pour l'Air Traffic Management (ATM).La Traçabilité Numérique des Bagages : Solution basée sur QR Code pour éliminer les pertes de bagages et améliorer l'expérience passager.🎯 Objectifs du ProjetLe système intégré (Fullstack AI) adresse deux problématiques critiques :ProblématiqueObjectif PrincipalSolution TechnologiqueSécurité/OpérationsAméliorer la prise de décision de l'ATC face aux risques météorologiques (turbulence, givrage, vents de travers).Modèles de Météo IA (GraphCast, Pangu-Weather) exposés via FastAPI.Expérience Client/LogistiqueRéduire les pertes et les retards de bagages, en offrant une transparence totale au passager.Traçabilité des Bagages par QR Code (Base de données PostgreSQL + API Express.js).🛠️ Stack TechniqueCe projet est une application Fullstack micro-services :ComposantTechnologieRôleFrontendReactJSConsole ATC pour la Météo et Interface de Suivi Passager (Bagages).Backend APIExpress.js (Node.js)Gestion des utilisateurs, authentification, API pour les logs de Bagages et la façade applicative.Microservice IAFastAPI (Python)Serveur d'inférence pour les modèles GraphCast/Pangu-Weather et post-traitement des données.Base de DonnéesPostgreSQLStockage optimisé des logs de scan de bagages et des prédictions météorologiques spatio-temporelles.ConteneurisationDockerPour garantir un environnement de développement et de déploiement cohérent.🚀 Démarrage Rapide (Configuration Locale)Suivez ces étapes pour lancer l'application en mode développement.PrérequisAssurez-vous d'avoir installé les logiciels suivants :Node.js (LTS)Python 3.10+Docker et Docker Compose1. Cloner le Dépôtgit clone [https://www.wordreference.com/fren/d%C3%A9p%C3%B4t](https://www.wordreference.com/fren/d%C3%A9p%C3%B4t)
cd projet-anac-aviation

2. Configuration des Variables d'EnvironnementCréez un fichier .env à la racine du projet et configurez les variables nécessaires (exemple) :# .env file

# --- CONFIGURATION BASE DE DONNÉES (POSTGRESQL) ---
DB_HOST=db_pg
DB_PORT=5432
DB_USER=anac_user
DB_PASSWORD=secret_password
DB_NAME=anac_db

# --- CONFIGURATION AUTHENTIFICATION / JWT ---
JWT_SECRET_KEY=votre_cle_secrete_jwt

3. Lancer les Services via Docker ComposeNous utilisons Docker Compose pour orchestrer le Frontend, le Backend (Express/FastAPI) et la base de données PostgreSQL.# Construire les images et démarrer tous les conteneurs
docker-compose up --build

Services disponibles après le démarrage :Frontend (Interface Utilisateur) : http://localhost:3000Backend API (Express.js) : http://localhost:8080 (Pour les endpoints Bagages/Auth)Microservice IA (FastAPI) : http://localhost:8000 (Pour les endpoints Météo)4. Initialisation de la Base de DonnéesUne fois le conteneur PostgreSQL démarré, vous devez exécuter les scripts d'initialisation pour créer les tables (Bagages, Météo, etc.).Vous pouvez vous connecter au conteneur DB :docker exec -it [ID ou Nom du conteneur DB] psql -U anac_user anac_db

Puis exécutez les scripts SQL :-- Création des tables de base (à adapter si vous utilisez un ORM comme Prisma)
-- Exemple : tables 'bags', 'scan_logs', 'predictions', 'airports'
\i init_db.sql

🛄 Traçabilité des Bagages (Focus Technique)La fonctionnalité de traçabilité est gérée par le service Express.js et PostgreSQL.Modèle de Données CléTableRôleChamps ClésbagsInformations sur le bagage et le propriétaire.qr_code_id (PK), passenger_id, flight_number, destination_airport.scan_logsHistorique des scans du bagage.log_id (PK), qr_code_id (FK), timestamp, location (Aéroport/Terminal), operator_id.API de Scan (Backend Express.js)L'endpoint principal pour l'enregistrement des mouvements est : POST /api/bag/scan Corps de la requête (JSON) :{
  "qrCodeId": "AERO-LFW-123456",
  "location": "LFW - Tapis Déchargement 3",
  "operatorId": "OPR-007"
}

⛈️ Météo IA (Focus Technique)Le service Python/FastAPI gère le calcul des prédictions.EndpointMéthodeDescription/api/weather/predictGETDéclenche l'inférence du modèle GraphCast et stocke les résultats./api/weather/tma/:airportGETRécupère les prédictions localisées pour la Zone Terminale (TMA) d'un aéroport donné (ex. vent, visibilité).🗺️ Feuille de Route (V2)Ce projet est organisé en deux phases majeures. Les tâches sont détaillées dans le document feuille_de_route_v2.tex.Phase 1 : Fondations et CoreBlocTâches PrincipalesÉtatA - ArchitectureDéfinition des spécifications (Météo/Bagages).À FaireB - Météo IATest d'inférence, ingestion des données dans PostgreSQL.En CoursC - Traçabilité BagagesModèle de données, API de scan, interface passager de base.À FaireD - IntégrationConteneurisation (Docker), connexion Fullstack.À FairePhase 2 : Déploiement et OptimisationBlocTâches PrincipalesÉtatE - DéploiementMise en production du service IA/Bagages, fine-tuning des modèles.À PlanifierF - CommercialisationAPI B2B, audit de sécurité, documentation.À Planifier🤝 ContributionNous accueillons les contributions !Forkez le dépôt.Créez une branche pour votre fonctionnalité (git checkout -b feat/nom-de-la-fonctionnalite).Committez vos changements (git commit -m 'feat: Ajout de la nouvelle fonctionnalité X').Poussez vers la branche (git push origin feat/nom-de-la-fonctionnalite).Ouvrez une Pull Request.Développé par :$$Votre Nom d'Équipe$$| Supervisé par : ANAC Togo
