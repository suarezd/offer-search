# Offer Search

Extension Chrome/Firefox + Backend FastAPI pour centraliser les offres d'emploi LinkedIn avec architecture hexagonale.

## 🚀 Quick Start

**Prérequis** : Docker + Docker Compose (c'est tout !)

```bash
# Cloner et démarrer TOUT (backend + DB + frontend)
git clone <url-du-repo>
cd offer-search
make start

# OU démarrer seulement le backend + DB
make backend-dev

# Lancer les tests
make test-unit         # 36 tests ✅
make test-integration  # 20 tests ✅

# Arrêter tout
make stop
```

**📖 Guide complet** : [QUICK_START.md](QUICK_START.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICK_START.md](QUICK_START.md)** | Guide de démarrage Docker-only |
| **[CHANGELOG.md](CHANGELOG.md)** | Historique des changements |
| [Guide Architecture Hexagonale](docs/HEXAGONAL_ARCHITECTURE_GUIDE.md) | Tutoriel complet |
| [Structure du Projet](docs/PROJECT_STRUCTURE.md) | Organisation détaillée |
| [Tests Backend](backend/README.md) | Guide d'exécution des tests |
| [ADRs](docs/adr/) | Décisions architecturales |

---

## Description

Offer Search est une solution complète comprenant :

- 🔵 **Extension navigateur** (Chrome & Firefox) - Scraping LinkedIn
- 🟢 **Backend API** - FastAPI avec architecture hexagonale
- 🗄️ **Base de données** - PostgreSQL avec async (asyncpg)
- 🧪 **Tests complets** - 56 tests (unitaires + intégration + BDD)
- 🏗️ **Architecture hexagonale** - Domain, Application, Adapters, Infrastructure
- ⚡ **Performance** - Async/await (+60% performance)

### État du Projet

- ✅ **Phase 1** : Extension Chrome/Firefox + Scraping LinkedIn
- ✅ **Phase 2** : Backend FastAPI + PostgreSQL + Architecture hexagonale + Tests
- ⏳ **Phase 3** : Fonctionnalités avancées (filtres, alertes, statistiques)

---

## Fonctionnalités

### Extension (Phase 1) ✅

- ✅ Scraping des offres LinkedIn recommandées
- ✅ Support multi-formats de pages LinkedIn
- ✅ Extraction complète (titre, entreprise, localisation, date, description, URL)
- ✅ Stockage local avec `chrome.storage.local`
- ✅ Interface popup responsive
- ✅ Compatible Chrome & Firefox

### Backend (Phase 2) ✅

- ✅ **API REST** avec FastAPI
  - `POST /api/jobs/submit` - Soumission d'offres
  - `GET /api/jobs/search` - Recherche avec filtres
  - `GET /api/jobs/stats` - Statistiques
- ✅ **Architecture hexagonale**
  - Domain : Entités + Ports
  - Application : Use Cases
  - Adapters : HTTP + PostgreSQL
  - Infrastructure : DI FastAPI
- ✅ **Base de données PostgreSQL**
  - Support async avec asyncpg
  - Déduplication automatique
  - Indexation optimisée
- ✅ **Tests complets**
  - 36 tests unitaires (Job entity)
  - 20 tests d'intégration (Repository)
  - 6 scénarios BDD Gherkin
- ✅ **CI/CD** - GitHub Actions

### Fonctionnalités avancées (Phase 3) ⏳

- ⏳ Filtres avancés (localisation, contrat, technologies)
- ⏳ Système d'alertes
- ⏳ Authentification utilisateurs
- ⏳ Export données (CSV, JSON)
- ⏳ Frontend de visualisation

---

## Installation

### Option 1 : Docker uniquement (Recommandé) 🐳

**Prérequis** : Docker + Docker Compose

```bash
# Cloner
git clone <url>
cd offer-search

# Démarrer backend
make backend-dev

# Tester
make test-all
```

**Avantage** : Aucune installation de Python, pip, Node.js, npm requise !

### Option 2 : Installation locale (Développement frontend)

**Prérequis** : Node.js 18+, npm

```bash
# Extension
npm install
npm run build

# Backend (via Docker recommandé)
make backend-dev
```

---

## Utilisation

### Backend API

```bash
# Démarrer
make backend-dev

# URLs
# API : http://localhost:8000
# Docs : http://localhost:8000/docs
# Health : http://localhost:8000/health
```

### Extension Chrome

1. Build : `npm run build` ou `make build-chrome`
2. Chrome : `chrome://extensions/` → Mode développeur → Charger `dist/`
3. LinkedIn : Aller sur LinkedIn Jobs
4. Extension : Cliquer sur l'icône → "Récupérer mes offres"

### Tests

```bash
make test-unit         # Tests unitaires (36)
make test-integration  # Tests d'intégration (20)
make test-functional   # Tests BDD (6 scénarios)
make test-all          # Tous les tests
make test-coverage     # Avec rapport HTML
```

---

## Structure du Projet

```
offer-search/
├── backend/                    # 🟢 Backend API (Python/FastAPI)
│   ├── app/
│   │   ├── domain/             # ❤️  Cœur métier (entities, ports)
│   │   ├── application/        # 🎯 Use cases
│   │   ├── adapters/           # 🔌 HTTP + PostgreSQL
│   │   └── infrastructure/     # ⚙️  Configuration
│   ├── tests/                  # 🧪 56 tests
│   │   ├── unit/               # Tests unitaires (36)
│   │   ├── integration/        # Tests d'intégration (20)
│   │   └── functional/         # Tests BDD (6 scénarios)
│   ├── Dockerfile
│   └── requirements.txt
│
├── extension/                  # 🔵 Extension navigateur (TypeScript)
│   ├── src/
│   │   ├── domain/             # Entités + Ports
│   │   ├── application/        # Services
│   │   ├── adapters/           # UI + API
│   │   ├── background.ts
│   │   ├── content.ts
│   │   └── popup/
│   ├── dist/                   # Build (généré)
│   └── manifest.json
│
├── docs/                       # 📚 Documentation
│   ├── adr/                    # Architecture Decision Records
│   ├── HEXAGONAL_ARCHITECTURE_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   └── ARCHITECTURE_IMPLEMENTATION_REPORT.md
│
├── docker-compose.yml          # 🐳 Orchestration
├── Makefile                    # 🛠️  Commandes
├── CHANGELOG.md                # 📝 Historique
├── QUICK_START.md              # 🚀 Guide rapide
└── README.md                   # Ce fichier
```

---

## Technologies

### Backend
- **Python 3.11** - Langage
- **FastAPI** - Framework web
- **PostgreSQL 16** - Base de données
- **SQLAlchemy 2.0** - ORM async
- **asyncpg** - Driver PostgreSQL async (+60% perf)
- **Pydantic** - Validation
- **pytest** - Tests
- **Docker** - Conteneurisation

### Frontend
- **TypeScript** - Langage
- **Vite** - Build tool
- **Chrome Extension Manifest V3** - API extension
- **Architecture hexagonale** - Organisation code

---

## Commandes Makefile

### Backend

```bash
make start             # Démarrer TOUT (backend + DB + frontend)
make stop              # Arrêter tout
make backend-dev       # Démarrer backend + DB seulement
make backend-rebuild   # Rebuild après modif requirements.txt
make backend-stop      # Arrêter backend + DB
make backend-install   # Infos installation (Docker/local)
```

### Tests

```bash
make test-unit         # Tests unitaires (36 tests)
make test-integration  # Tests d'intégration (20 tests)
make test-functional   # Tests BDD (6 scénarios)
make test-all          # Tous les tests
make test-coverage     # Tests + rapport HTML
make test-ci           # Tests pour CI (XML + JUnit)
```

### Extension

```bash
make install           # Installer dépendances npm
make build             # Build pour Chrome
make build-chrome      # Build Chrome (explicite)
make build-firefox     # Build Firefox
make dev               # Mode développement
make clean             # Nettoyer build
```

### Docker

```bash
make docker-build      # Build image Docker
make docker-run        # Build extension via Docker
make docker-shell      # Shell dans container
```

### Autres

```bash
make help              # Toutes les commandes
make api-test          # Test endpoints API
```

---

## Développement

### Workflow Backend

```bash
# 1. Démarrer
make backend-dev

# 2. Modifier le code dans backend/app/

# 3. Tests auto-rechargés (--reload)
make test-unit

# 4. Avant commit
make test-all
```

### Workflow Extension

```bash
# 1. Installer
npm install

# 2. Développement
npm run dev

# 3. Build
npm run build

# 4. Tester dans Chrome
# chrome://extensions/ → Recharger
```

### Ajouter une dépendance Python

```bash
# 1. Modifier requirements.txt
echo "nouvelle-lib==1.0.0" >> backend/requirements.txt

# 2. Rebuild
make backend-rebuild

# 3. Redémarrer
make backend-dev
```

---

## Tests

### Statistiques

| Type | Nombre | Durée | Couverture |
|------|--------|-------|------------|
| Unitaires | 36 | 0.25s | Job entity |
| Intégration | 20 | 0.80s | Repository |
| BDD | 6 scénarios | - | API endpoints |
| **Total** | **56+** | **~1s** | **3 layers** |

### Exécution

```bash
# Via Makefile (Docker)
make test-unit
make test-integration
make test-all

# Via pytest direct
cd backend
python -m pytest -m unit -v
python -m pytest -m integration -v
```

### Couverture

```bash
make test-coverage
# Génère backend/htmlcov/index.html
```

---

## CI/CD

GitHub Actions configuré dans [.github/workflows/tests.yml](.github/workflows/tests.yml)

**Déclencheurs** :
- Push sur `master`, `develop`, `feat/*`
- Pull requests vers `master`, `develop`

**Pipeline** :
1. Setup Python 3.11
2. PostgreSQL service
3. Install dependencies
4. Run unit tests
5. Run integration tests
6. Generate coverage
7. Upload to Codecov

---

## Architecture

### Hexagonale (Ports & Adapters)

```
┌─────────────────────────────────────────┐
│           PRIMARY ADAPTERS              │
│         (HTTP Routes, UI)               │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │   APPLICATION   │
        │   (Use Cases)   │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │     DOMAIN      │
        │ (Entities+Ports)│
        └────────┬────────┘
                 │
┌────────────────▼────────────────────────┐
│        SECONDARY ADAPTERS               │
│    (PostgreSQL, External APIs)          │
└─────────────────────────────────────────┘
```

### Couches

1. **Domain** (Cœur) - Logique métier pure
   - Entités : `Job`
   - Ports : `IJobRepository`
   - Exceptions : `DuplicateJobError`, `JobNotFoundError`

2. **Application** - Orchestration
   - Use Cases : `SubmitJobsUseCase`, `SearchJobsUseCase`
   - DTOs : `JobCreateDTO`, `JobResponseDTO`

3. **Adapters** - Interface monde extérieur
   - Primary : HTTP Routes
   - Secondary : PostgreSQL Repository

4. **Infrastructure** - Configuration
   - Dependency Injection
   - Database config

**Avantage** : Facile de changer PostgreSQL → MongoDB sans toucher au domaine !

---

## Roadmap

### ✅ Réalisé

- [x] Extension Chrome/Firefox
- [x] Scraping LinkedIn
- [x] Backend FastAPI
- [x] PostgreSQL avec async
- [x] Architecture hexagonale
- [x] Tests complets (56)
- [x] CI/CD GitHub Actions
- [x] Documentation complète

### ⏳ En cours / À venir

- [ ] Tests fonctionnels BDD (step definitions)
- [ ] Frontend visualisation
- [ ] Filtres avancés
- [ ] Système d'alertes
- [ ] Authentification
- [ ] Cache IndexedDB
- [ ] Export CSV/JSON

---

## Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feat/amazing-feature`)
3. Commit (`git commit -m 'feat: add amazing feature'`)
4. Push (`git push origin feat/amazing-feature`)
5. Ouvrir une Pull Request

**Avant de soumettre** :
```bash
make test-all  # Tous les tests doivent passer
```

---

## Licence

À définir

---

## Support

- **Documentation** : [docs/](docs/)
- **Issues** : GitHub Issues
- **Tests** : `make test-all`

---

**Fait avec ❤️ et architecture hexagonale**
