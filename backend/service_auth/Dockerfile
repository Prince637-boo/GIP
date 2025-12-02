    # Utilise une image Python légère comme base
    FROM python:3.11-slim

    # Définit le répertoire de travail dans le conteneur
    WORKDIR /app

    # Installe uv et les dépendances système nécessaires

    RUN apt-get update && apt-get install -y curl python3-dev && rm -rf /var/lib/apt/lists/*
    
    # RUN pip install uv

    # # Copie les fichiers de gestion des dépendances 
    # COPY uv.lock .
    # COPY pyproject.toml . 

    COPY requirements.txt .

    RUN pip install --no-cache-dir -r requirements.txt

    # Installe les dépendances
    # RUN uv pip sync uv.lock

    # Copie le reste du code de l'application
    COPY . .

    # Expose le port sur lequel l'application s'exécute
    EXPOSE 8000

    # Commande pour lancer le serveur Uvicorn au démarrage du conteneur
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
