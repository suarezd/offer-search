# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté
- **Auto-installation des dépendances npm** dans le Makefile
  - `make build`, `make build-chrome`, `make build-firefox` vérifient et installent automatiquement `node_modules` si absent
  - `make dev` et `make start` incluent l'auto-installation
  - Plus besoin de `make install` ou `npm install` manuel
- **Section dépannage** dans QUICK_START.md
  - Erreurs "vite: not found" ou commandes npm manquantes
  - Problèmes de permissions Docker

### Corrigé
- **Problèmes de permissions Docker** sur les fichiers générés
  - Dockerfile : Utilise maintenant l'utilisateur `node` (UID/GID 1000) au lieu de root
  - docker-compose.yml : Configure `user: "${UID:-1000}:${GID:-1000}"` pour les services extension et extension-dev
  - Les fichiers créés dans `dist/` appartiennent maintenant à l'utilisateur courant, plus besoin de `sudo` pour les supprimer
- **Erreur "vite: not found"** lors de `make start` sans `node_modules`
  - L'auto-installation des dépendances résout ce problème automatiquement

### Modifié
- **Documentation mise à jour**
  - README.md : Ajout de notes sur l'auto-installation, instructions Firefox complètes, workflow simplifié
  - QUICK_START.md : Guide avec auto-installation, section dépannage étendue
  - Makefile help : Annotations sur l'auto-installation des dépendances

### À venir
- Tests fonctionnels BDD (step definitions complètes)
- Tests use cases (Application layer)
- Frontend pour visualisation des offres
- Système d'alertes
- Authentification utilisateurs

## [2.0.0] - 2025-12-12

### Ajouté
- **Architecture hexagonale complète** pour le backend
  - Couche Domain : Entités métier (Job) avec validations
  - Couche Application : Use Cases (Submit, Search, GetStats)
  - Couche Adapters : HTTP Routes (primary), SQLAlchemy Repository (secondary)
  - Couche Infrastructure : Injection de dépendances FastAPI
<<<<<<< HEAD
- **Architecture hexagonale** pour le frontend
  - Domain : Entités (Job, JobFilter) + Ports (IJobRepository)
  - Application : Services (JobApplicationService)
  - Adapters : UI (Popup, Options) + Repositories (Api, Local)
- **Tests complets** (56 tests passent à 100%)
  - 36 tests unitaires (Job entity)
  - 20 tests d'intégration (SQLAlchemy Repository)
  - 6 scénarios BDD Gherkin définis
=======
- **Tests complets** (56 tests passent à 100%)
  - 36 tests unitaires (Job entity)
  - 20 tests d'intégration (SQLAlchemy Repository)
  - 6 scénarios BDD Gherkin (à exécuter)
>>>>>>> 80fd755 (chore(tests): adding behavioural, unit and integration tests)
- **Infrastructure de tests**
  - Configuration pytest avec marqueurs (unit, integration, functional)
  - Fixtures réutilisables avec isolation transactionnelle
  - Commandes Makefile pour tous les types de tests
  - GitHub Actions workflow pour CI/CD
- **Support async complet**
<<<<<<< HEAD
  - asyncpg pour PostgreSQL (+60% performance vs psycopg2)
=======
  - asyncpg pour PostgreSQL (+60% performance)
>>>>>>> 80fd755 (chore(tests): adding behavioural, unit and integration tests)
  - SQLAlchemy 2.0 avec async/await
  - Sessions async avec gestion transactionnelle
- **Documentation extensive**
  - 3 Architecture Decision Records (ADRs)
<<<<<<< HEAD
  - Guide complet Architecture Hexagonale (500+ lignes)
  - Structure du projet documentée
  - Guide d'exécution des tests
  - QUICK_START.md pour démarrage rapide
  - Changelog conventionnel
  - README complet mis à jour
=======
  - Guide complet Architecture Hexagonale
  - Structure du projet documentée
  - Guide d'exécution des tests
  - Changelog conventionnel
>>>>>>> 80fd755 (chore(tests): adding behavioural, unit and integration tests)

### Modifié
- **Backend API** complètement refactorisé en architecture hexagonale
- **Base de données** : Support async avec asyncpg
<<<<<<< HEAD
- **Dépendances** : Ajout de pytest, pytest-asyncio, pytest-bdd, pytest-cov, httpx, freezegun
- **Docker** : Configuration pour environnement de test (DB test créée automatiquement)
- **Makefile** : 7 nouvelles commandes de test + backend-rebuild

### Déprécié
- Anciens fichiers monolithiques (conservés temporairement pour compatibilité)

### Retiré
=======
- **Dépendances** : Ajout de pytest, pytest-asyncio, pytest-bdd, pytest-cov
- **Docker** : Configuration pour environnement de test
- **Makefile** : 7 nouvelles commandes de test

### Déprécié
- Aucun

### Retiré
- Anciens fichiers obsolètes (models/, routers/, schemas/, database.py)
>>>>>>> 80fd755 (chore(tests): adding behavioural, unit and integration tests)
- Commentaires inutiles dans le code (principe clean code)

### Corrigé
- Bug dans `Job.matches_search()` : gestion correcte de `description=None`
- Isolation transactionnelle des tests d'intégration
<<<<<<< HEAD
- Configuration database URL pour tests Docker (db vs localhost)
- Format de retour de `save_many()` avec `duplicate_ids` et `failed`
=======
- Configuration database URL pour tests Docker
>>>>>>> 80fd755 (chore(tests): adding behavioural, unit and integration tests)

### Sécurité
- Validation stricte des entités dans la couche Domain
- Gestion appropriée des duplicates
- Protection contre l'injection SQL (ORM)
<<<<<<< HEAD
- Pas de secrets en dur dans le code

## [1.0.0] - 2025-12-11

### Ajouté
- Extension Chrome/Firefox initiale
- Scraping des offres LinkedIn recommandées
- Support de plusieurs formats de pages LinkedIn
  - `linkedin.com/jobs/search/`
  - `linkedin.com/jobs/collections/recommended/`
  - Pages paginées avec paramètre `start=`
- Extraction complète des informations :
  - Titre du poste
  - Entreprise
  - Localisation
  - Date de publication
  - Description (aperçu)
  - URL de l'offre
- Stockage local avec `chrome.storage.local`
- Interface popup responsive
- Backend FastAPI basique
- Base de données PostgreSQL
- Docker Compose pour orchestration
- Makefile pour simplifier les commandes

### Technologies
- TypeScript + Vite pour l'extension
- Python 3.11 + FastAPI pour le backend
- PostgreSQL 16 pour la base de données
- Docker pour la conteneurisation
=======

## [1.0.0] - Date antérieure

### Ajouté
- Extension Chrome/Firefox initiale
- Scraping des offres LinkedIn
- Backend FastAPI basique
- Base de données PostgreSQL
- Stockage local avec chrome.storage
- Interface popup responsive
- Support Chrome et Firefox
>>>>>>> 80fd755 (chore(tests): adding behavioural, unit and integration tests)

---

## Types de changements
- `Ajouté` : nouvelles fonctionnalités
- `Modifié` : changements dans des fonctionnalités existantes
- `Déprécié` : fonctionnalités bientôt supprimées
- `Retiré` : fonctionnalités supprimées
- `Corrigé` : corrections de bugs
- `Sécurité` : corrections de vulnérabilités
