# Utilise une image Python légère comme base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Installe curl pour les healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install uv

# Copie les fichiers de gestion de dépendances
COPY uv.lock .
COPY pyproject.toml .

# Installe les dépendances avec uv
RUN uv sync --frozen

# Copie le reste du code de l'application
COPY . .

# Expose le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande pour lancer le serveur Uvicorn au démarrage du conteneur
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
