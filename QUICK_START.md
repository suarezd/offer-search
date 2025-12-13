# Quick Start - Offer Search

Guide de démarrage rapide pour développer avec Docker uniquement (pas besoin de Python/Node.js en local).

## Prérequis

- ✅ **Docker** et **Docker Compose** installés
- ✅ **Make** installé (généralement préinstallé sur Linux/macOS, ou via Git Bash sur Windows)

**C'est tout !** Pas besoin de Python, pip, Node.js, ou npm sur votre machine.

## 🚀 Démarrage rapide

```bash
# 1. Cloner le projet
git clone <url>
cd offer-search

# 2. Voir toutes les commandes disponibles
make help

# 3. Démarrer TOUT (backend + DB + frontend)
make start

# OU démarrer seulement le backend
make backend-dev

# 4. Vérifier que tout fonctionne
make test-unit           # 36 tests unitaires
make test-integration    # 20 tests d'intégration

# 5. Arrêter tous les services
make stop
```

## 📋 Commandes essentielles

### Backend + Frontend (tout via Docker)

```bash
# Démarrer TOUT (backend + DB + frontend)
make start              # Recommandé !

# OU démarrer seulement backend + PostgreSQL
make backend-dev

# Rebuild après changement de dépendances
make backend-rebuild

# Arrêter tous les services
make stop               # Arrête tout
make backend-stop       # Arrête seulement backend + DB

# Voir les logs
docker compose logs -f api
```

### Tests (tout via Docker)

```bash
# Tests unitaires (rapides, pas de DB)
make test-unit

# Tests d'intégration (avec DB PostgreSQL)
make test-integration

# Tous les tests
make test-all

# Tests avec couverture
make test-coverage

# Tests pour CI
make test-ci
```

### Extension navigateur

```bash
# Build extension (via Docker)
make docker-build        # Build l'image Node.js
make docker-run          # Build l'extension

# Ou avec npm local si installé
make install
make build-chrome
make build-firefox
```

## 🔧 Workflow de développement

### Backend

```bash
# 1. Démarrer l'environnement
make backend-dev

# 2. Faire vos modifications dans backend/app/

# 3. Les tests se rechargent automatiquement
make test-unit

# 4. Avant de commit
make test-all
```

### Ajouter une dépendance Python

```bash
# 1. Ajouter la dépendance dans backend/requirements.txt
echo "nouvelle-lib==1.0.0" >> backend/requirements.txt

# 2. Rebuild l'image Docker
make backend-rebuild

# 3. Redémarrer
make backend-stop
make backend-dev
```

## 🏗️ Architecture

```
offer-search/
├── backend/              # API FastAPI (Python)
│   ├── app/
│   │   ├── domain/       # Cœur métier (entities, ports)
│   │   ├── application/  # Use cases
│   │   ├── adapters/     # HTTP, PostgreSQL
│   │   └── infrastructure/
│   ├── tests/            # 56 tests
│   └── Dockerfile        # Image Python 3.11
├── extension/            # Extension navigateur (TypeScript)
├── docker-compose.yml    # Orchestration
└── Makefile             # Toutes les commandes
```

## 🐳 Services Docker

```bash
# Voir les services en cours
docker compose ps

# Logs d'un service
docker compose logs -f api
docker compose logs -f db

# Shell dans un container
docker exec -it offer-search-api-1 /bin/bash
docker exec -it offer-search-db-1 psql -U offeruser -d offerdb

# Nettoyer tout
docker compose down -v  # -v supprime les volumes
```

## 📊 Tests

### Exécution

```bash
# Unitaires (0.25s)
make test-unit
# ✅ 36 tests passent

# Intégration (0.80s)
make test-integration
# ✅ 20 tests passent

# BDD/Fonctionnels (à venir)
make test-functional
# ⏳ 6 scénarios Gherkin
```

### Couverture

```bash
make test-coverage
# Génère backend/htmlcov/index.html
```

## 🔗 URLs utiles

- **API** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs
- **Health** : http://localhost:8000/health
- **PostgreSQL** : localhost:5432

## 🆘 Dépannage

### Les tests échouent

```bash
# Vérifier que les services tournent
docker compose ps

# Relancer la DB
make backend-stop
make backend-dev

# Nettoyer la DB de test
docker exec offer-search-db-1 psql -U offeruser -d offerdb -c "DROP DATABASE IF EXISTS offer_search_test; CREATE DATABASE offer_search_test;"
```

### L'image Docker est obsolète

```bash
make backend-rebuild
make backend-dev
```

### Réinitialiser complètement

```bash
# Arrêter tout
make backend-stop

# Supprimer volumes
docker compose down -v

# Rebuild
make backend-rebuild

# Redémarrer
make backend-dev
```

## 📚 Documentation

- [README principal](README.md)
- [CHANGELOG](CHANGELOG.md)
- [Architecture Hexagonale](docs/HEXAGONAL_ARCHITECTURE_GUIDE.md)
- [Structure du projet](docs/PROJECT_STRUCTURE.md)
- [Tests Backend](backend/README.md)
- [ADRs](docs/adr/)

## ✅ Checklist avant commit

```bash
# 1. Tests passent
make test-all

# 2. Code formaté (si configuré)
# make format

# 3. Pas de secrets
git status
git diff

# 4. Commit
git add .
git commit -m "feat: description"
```

---

**💡 Astuce** : Toutes les commandes sont dans `make help`
