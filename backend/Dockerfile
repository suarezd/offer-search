FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copie depuis le dossier backend/ (contexte de build = racine du projet)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Railway injecte automatiquement la variable $PORT
# Utilise --no-access-log pour réduire les logs en production
# Retire --reload car ce n'est pas nécessaire en production
# Utiliser sh -c pour permettre la substitution de variables
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
