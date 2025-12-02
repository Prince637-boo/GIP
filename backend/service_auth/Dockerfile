# Utilise une image Python légère comme base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de gestion des dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande pour lancer le serveur Uvicorn au démarrage du conteneur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
