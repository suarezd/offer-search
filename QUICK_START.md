# Quick Start - Offer Search

Guide de démarrage rapide pour développer avec Docker uniquement (pas besoin de Python/Node.js en local).

## Prérequis

- ✅ **Docker** et **Docker Compose** installés
- ✅ **Make** installé (généralement préinstallé sur Linux/macOS, ou via Git Bash sur Windows)

**C'est tout !** Pas besoin de Python, pip, Node.js, ou npm sur votre machine.

### 💻 Installation selon votre OS

#### Linux / macOS
Docker et Make sont généralement préinstallés ou facilement installables via votre gestionnaire de paquets.

#### Windows
Vous avez **3 options** pour utiliser Offer Search sur Windows :

**Option 1 : Docker Desktop + Git Bash (Recommandé)**
- Installer [Docker Desktop pour Windows](https://www.docker.com/products/docker-desktop/)
- Installer [Git for Windows](https://git-scm.com/download/win) (inclut Git Bash avec `make`)
- Utiliser Git Bash pour lancer toutes les commandes `make`

**Option 2 : WSL2 (Windows Subsystem for Linux)**
- Installer WSL2 avec Ubuntu
- Suivre les instructions Linux ci-dessus dans WSL2
- Plus natif et performant pour le développement

**Option 3 : PowerShell sans Make**
Si vous ne voulez pas utiliser Git Bash, utilisez les commandes npm directement :
```powershell
# Au lieu de: make build
npm install
npm run build

# Au lieu de: make backend-dev
docker compose up -d db api
```

**Dépannage Windows :**
- **Make non reconnu** : Installer Git for Windows ou utiliser WSL2
- **Docker ne démarre pas** : Vérifier que la virtualisation est activée dans le BIOS
- **Permissions Docker** : Lancer PowerShell/Git Bash en administrateur

## 🚀 Démarrage rapide

```bash
# 1. Cloner le projet
git clone <url>
cd offer-search

# 2. Voir toutes les commandes disponibles
make help

# 3. Démarrer TOUT (backend + DB + frontend)
make start              # Auto-installe les dépendances npm si besoin

# OU démarrer seulement le backend
make backend-dev

# 4. Vérifier que tout fonctionne
make test-unit           # 36 tests unitaires
make test-integration    # 20 tests d'intégration

# 5. Arrêter tous les services
make stop
```

**💡 Note** : Les commandes `make start`, `make build`, et `make dev` installent automatiquement les dépendances npm si `node_modules` n'existe pas !

## 📋 Commandes essentielles

### Backend + Frontend (tout via Docker)

```bash
# Démarrer TOUT (backend + DB + frontend)
make start              # Recommandé ! Auto-installe les dépendances

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
# Build extension (auto-installe les dépendances si besoin)
make build              # Chrome (auto-installe npm packages)
make build-firefox      # Firefox (auto-installe npm packages)

# Build via Docker (sans installation npm locale)
make docker-build       # Build l'image Node.js
make docker-run         # Build l'extension

# Installation manuelle (optionnelle)
make install            # Équivalent à npm install
```

**💡 Nouveau** : Plus besoin de `npm install` manuel ! Les commandes de build vérifient automatiquement si `node_modules` existe.

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

## 🌐 Utilisation de l'extension

L'extension supporte maintenant **deux sources** de scraping :

### LinkedIn
1. Navigue vers [LinkedIn Jobs](https://linkedin.com/jobs/search/)
2. Ouvre l'extension
3. Clique sur "Récupérer les offres"

### Indeed
1. Navigue vers [Indeed FR](https://fr.indeed.com/jobs) ou [Indeed US](https://indeed.com/jobs)
2. Ouvre l'extension
3. Clique sur "Récupérer les offres"

### Filtres
- **Recherche** : Par titre, technologie, description
- **Localisation** : Ville ou Remote
- **Entreprise** : Nom de l'entreprise
- **Source** : LinkedIn, Indeed, ou toutes les sources

**💡 Astuce** : L'extension détecte automatiquement la source selon l'URL active !

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

### Erreur "vite: not found" ou commande npm manquante

```bash
# Les dépendances s'installent normalement automatiquement
# Si besoin, forcer l'installation :
make install

# Ou supprimer et recréer node_modules
rm -rf node_modules
make build  # Réinstalle automatiquement
```

### Problèmes de permissions (fichiers appartenant à root)

**Note** : Ce problème a été résolu (voir [CHANGELOG.md](CHANGELOG.md)). Les nouvelles installations ne devraient plus rencontrer ce problème.

Si vous rencontrez toujours des fichiers root dans `dist/` :

```bash
# Corriger les permissions avec Docker (sans sudo)
docker run --rm -v "$(pwd)/dist:/dist" alpine:latest chown -R 1000:1000 /dist

# Puis reconstruire l'image Docker avec les nouvelles permissions
make docker-build
make clean
make build
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
- [Guide des tests](TESTING.md)
- [CHANGELOG](CHANGELOG.md)
- [Architecture & ADRs](docs/adr/ADR.md)
- [Documentation backend](backend/README.md)
- [Documentation complète](docs/README.md)

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
