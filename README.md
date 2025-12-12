# Offer Search

Extension Chrome/Firefox + Backend FastAPI pour centraliser les offres d'emploi LinkedIn avec architecture hexagonale.

## 🚀 Quick Start

**Prérequis** : Docker + Docker Compose (c'est tout !)

```bash
# Cloner et démarrer TOUT (backend + DB + frontend)
git clone <url-du-repo>
cd offer-search
make start              # Auto-installe les dépendances frontend si nécessaire

# OU démarrer seulement le backend + DB
make backend-dev

# OU build l'extension uniquement
make build              # Auto-installe les dépendances si nécessaire

# Arrêter tout
make stop
```

**💡 Note** : Les dépendances npm sont installées automatiquement lors du premier `make start`, `make build`, ou `make dev`. Pas besoin de `npm install` manuel !

**📖 Guide complet** : [QUICK_START.md](QUICK_START.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICK_START.md](QUICK_START.md)** | Guide de démarrage Docker-only |
| **[CHANGELOG.md](CHANGELOG.md)** | Historique des changements |
| [Documentation complète](docs/README.md) | Architecture, guides, et ADRs |
| [Guide Architecture Hexagonale](docs/HEXAGONAL_ARCHITECTURE_GUIDE.md) | Tutoriel complet |
| [Structure du Projet](docs/PROJECT_STRUCTURE.md) | Organisation détaillée |
| [ADRs](docs/adr/) | Décisions architecturales |

---

## Description

Offer Search est une solution complète comprenant :

- 🔵 **Extension navigateur** (Chrome & Firefox) - Scraping LinkedIn
- 🟢 **Backend API** - FastAPI avec architecture hexagonale
- 🗄️ **Base de données** - PostgreSQL avec async (asyncpg)
- 🏗️ **Architecture hexagonale** - Domain, Application, Adapters, Infrastructure
- ⚡ **Performance** - Async/await (+60% performance)

### État du Projet

- ✅ **Phase 1** : Extension Chrome/Firefox + Scraping LinkedIn
- ✅ **Phase 2** : Backend FastAPI + PostgreSQL + Architecture hexagonale
- ⏳ **Phase 3** : Fonctionnalités avancées (tests, filtres, alertes, statistiques)

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
```

**Avantage** : Aucune installation manuelle de Python, pip, Node.js, npm requise !

### Option 2 : Installation locale (Développement frontend)

**Prérequis** : Node.js 18+, npm

```bash
# Extension - Les dépendances s'installent automatiquement
make build              # ou make build-firefox, make start, make dev

# Installation manuelle (optionnelle)
make install            # Équivalent à npm install

# Backend (via Docker recommandé)
make backend-dev
```

**💡 Nouveau** : Plus besoin de `npm install` manuel ! Les commandes `make build`, `make start`, et `make dev` installent automatiquement les dépendances si le dossier `node_modules` est absent.

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

1. Build : `make build` (auto-installe les dépendances)
2. Chrome : `chrome://extensions/` → Mode développeur → Charger `dist/`
3. LinkedIn : Aller sur LinkedIn Jobs
4. Extension : Cliquer sur l'icône → "Récupérer mes offres"

### Extension Firefox

1. Build : `make build-firefox` (auto-installe les dépendances)
2. Firefox : `about:debugging#/runtime/this-firefox` → Charger un module temporaire
3. Sélectionner : `dist/manifest.json`
4. LinkedIn : Aller sur LinkedIn Jobs
5. Extension : Cliquer sur l'icône → "Récupérer mes offres"

## Structure du Projet

```
offer-search/
├── backend/                    # 🟢 Backend API (Python/FastAPI)
│   ├── app/
│   │   ├── domain/             # ❤️  Cœur métier (entities, ports)
│   │   ├── application/        # 🎯 Use cases
│   │   ├── adapters/           # 🔌 HTTP + PostgreSQL
│   │   └── infrastructure/     # ⚙️  Configuration
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
make start             # Démarrer TOUT (backend + DB + frontend, auto-installe deps)
make stop              # Arrêter tout
make backend-dev       # Démarrer backend + DB seulement
make backend-rebuild   # Rebuild après modif requirements.txt
make backend-stop      # Arrêter backend + DB
make backend-install   # Infos installation (Docker/local)
```

## Développement

### Workflow Backend

```bash
# 1. Démarrer
make backend-dev

# 2. Modifier le code dans backend/app/

```

### Workflow Extension

```bash
# 1. Développement (auto-installe les dépendances si besoin)
make dev

# 2. Build (auto-installe les dépendances si besoin)
make build              # Pour Chrome
make build-firefox      # Pour Firefox

# 3. Tester dans Chrome
# chrome://extensions/ → Recharger

# 4. Tester dans Firefox
# about:debugging#/runtime/this-firefox → Recharger
```

**💡 Note** : Plus besoin de `npm install` manuel, c'est automatique !

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
- [x] CI/CD GitHub Actions
- [x] Documentation complète

### ⏳ En cours / À venir

- [ ] Frontend visualisation
- [ ] Filtres avancés
- [ ] Système d'alertes
- [ ] Authentification
- [ ] Cache IndexedDB
- [ ] Export CSV/JSON

---

## Contribution

Les contributions sont les bienvenues ! Veuillez lire notre [Code de Conduite](CODE_OF_CONDUCT.md) avant de contribuer.

1. Fork le projet
2. Créer une branche (`git checkout -b feat/amazing-feature`)
3. Commit (`git commit -m 'feat: add amazing feature'`)
4. Push (`git push origin feat/amazing-feature`)
5. Ouvrir une Pull Request

Pour plus de détails, consultez [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Support

- **Documentation** : [docs/](docs/)
- **Issues** : [GitHub Issues](https://github.com/suarezd/offer-search/issues)
- **Sécurité** : Pour signaler une vulnérabilité, consultez [SECURITY.md](SECURITY.md)

---

**Fait avec ❤️ et architecture hexagonale**
