#!/bin/bash

# Le nom de la dépendance à ajouter (exemple: "requests")
DEP_NAME=$1

if [ -z "$DEP_NAME" ]; then
    echo "Usage: ./add_dep_to_all.sh <package_name>"
    exit 1
fi

# Liste des répertoires de services 
SERVICES=("backend/app/api/service_auth_api" "backend/app/api/service_baggages_api" "backend/app/api/service_meteo_ia_api") 

for SERVICE_DIR in "${SERVICES[@]}"; do
    if [ -d "$SERVICE_DIR" ] && [ -f "$SERVICE_DIR/pyproject.toml" ]; then
        echo "----------------------------------------------------"
        echo "Ajout de '$DEP_NAME' dans le service: $SERVICE_DIR"
        cd "$SERVICE_DIR" || continue
        
        # Exécute uv add et met à jour pyproject.toml et uv.lock
        uv add "$DEP_NAME"
        
        # Retourne à la racine du projet pour la prochaine itération
        cd - || break
        echo "Terminé pour $SERVICE_DIR"
    else
        echo "Répertoire non valide ou pyproject.toml manquant: $SERVICE_DIR"
    fi
done

echo "----------------------------------------------------"
echo "Toutes les dépendances ont été mises à jour."
