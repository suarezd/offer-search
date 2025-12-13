# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### À venir
- Tests fonctionnels BDD (step definitions complètes)
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
- **Architecture hexagonale** pour le frontend
  - Domain : Entités (Job, JobFilter) + Ports (IJobRepository)
  - Application : Services (JobApplicationService)
  - Adapters : UI (Popup, Options) + Repositories (Api, Local)
- **Tests complets** (56 tests passent à 100%)
  - 36 tests unitaires (Job entity)
  - 20 tests d'intégration (SQLAlchemy Repository)
  - 6 scénarios BDD Gherkin définis
- **Infrastructure de tests**
  - Configuration pytest avec marqueurs (unit, integration, functional)
  - Fixtures réutilisables avec isolation transactionnelle
  - Commandes Makefile pour tous les types de tests
  - GitHub Actions workflow pour CI/CD
- **Support async complet**
  - asyncpg pour PostgreSQL (+60% performance vs psycopg2)
  - SQLAlchemy 2.0 avec async/await
  - Sessions async avec gestion transactionnelle
- **Documentation extensive**
  - 3 Architecture Decision Records (ADRs)
  - Guide complet Architecture Hexagonale (500+ lignes)
  - Structure du projet documentée
  - Guide d'exécution des tests
  - QUICK_START.md pour démarrage rapide
  - Changelog conventionnel
  - README complet mis à jour

### Modifié
- **Backend API** complètement refactorisé en architecture hexagonale
- **Base de données** : Support async avec asyncpg
- **Dépendances** : Ajout de pytest, pytest-asyncio, pytest-bdd, pytest-cov, httpx, freezegun
- **Docker** : Configuration pour environnement de test (DB test créée automatiquement)
- **Makefile** : 7 nouvelles commandes de test + backend-rebuild

### Déprécié
- Anciens fichiers monolithiques (conservés temporairement pour compatibilité)

### Retiré
- Commentaires inutiles dans le code (principe clean code)

### Corrigé
- Bug dans `Job.matches_search()` : gestion correcte de `description=None`
- Isolation transactionnelle des tests d'intégration
- Configuration database URL pour tests Docker (db vs localhost)
- Format de retour de `save_many()` avec `duplicate_ids` et `failed`

### Sécurité
- Validation stricte des entités dans la couche Domain
- Gestion appropriée des duplicates
- Protection contre l'injection SQL (ORM)
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

---

## Types de changements
- `Ajouté` : nouvelles fonctionnalités
- `Modifié` : changements dans des fonctionnalités existantes
- `Déprécié` : fonctionnalités bientôt supprimées
- `Retiré` : fonctionnalités supprimées
- `Corrigé` : corrections de bugs
- `Sécurité` : corrections de vulnérabilités
