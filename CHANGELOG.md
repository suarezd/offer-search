# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### À venir
- Tests fonctionnels BDD (6 scénarios)
- Tests use cases (Application layer)
- Frontend pour visualisation des offres
- Système d'alertes

## [2.0.0] - 2025-12-12

### Ajouté
- **Architecture hexagonale complète** pour le backend
  - Couche Domain : Entités métier (Job) avec validations
  - Couche Application : Use Cases (Submit, Search, GetStats)
  - Couche Adapters : HTTP Routes (primary), SQLAlchemy Repository (secondary)
  - Couche Infrastructure : Injection de dépendances FastAPI
- **Tests complets** (56 tests passent à 100%)
  - 36 tests unitaires (Job entity)
  - 20 tests d'intégration (SQLAlchemy Repository)
  - 6 scénarios BDD Gherkin (à exécuter)
- **Infrastructure de tests**
  - Configuration pytest avec marqueurs (unit, integration, functional)
  - Fixtures réutilisables avec isolation transactionnelle
  - Commandes Makefile pour tous les types de tests
  - GitHub Actions workflow pour CI/CD
- **Support async complet**
  - asyncpg pour PostgreSQL (+60% performance)
  - SQLAlchemy 2.0 avec async/await
  - Sessions async avec gestion transactionnelle
- **Documentation extensive**
  - 3 Architecture Decision Records (ADRs)
  - Guide complet Architecture Hexagonale
  - Structure du projet documentée
  - Guide d'exécution des tests
  - Changelog conventionnel

### Modifié
- **Backend API** complètement refactorisé en architecture hexagonale
- **Base de données** : Support async avec asyncpg
- **Dépendances** : Ajout de pytest, pytest-asyncio, pytest-bdd, pytest-cov
- **Docker** : Configuration pour environnement de test
- **Makefile** : 7 nouvelles commandes de test

### Déprécié
- Aucun

### Retiré
- Anciens fichiers obsolètes (models/, routers/, schemas/, database.py)
- Commentaires inutiles dans le code (principe clean code)

### Corrigé
- Bug dans `Job.matches_search()` : gestion correcte de `description=None`
- Isolation transactionnelle des tests d'intégration
- Configuration database URL pour tests Docker

### Sécurité
- Validation stricte des entités dans la couche Domain
- Gestion appropriée des duplicates
- Protection contre l'injection SQL (ORM)

## [1.0.0] - Date antérieure

### Ajouté
- Extension Chrome/Firefox initiale
- Scraping des offres LinkedIn
- Backend FastAPI basique
- Base de données PostgreSQL
- Stockage local avec chrome.storage
- Interface popup responsive
- Support Chrome et Firefox

---

## Types de changements
- `Ajouté` : nouvelles fonctionnalités
- `Modifié` : changements dans des fonctionnalités existantes
- `Déprécié` : fonctionnalités bientôt supprimées
- `Retiré` : fonctionnalités supprimées
- `Corrigé` : corrections de bugs
- `Sécurité` : corrections de vulnérabilités
