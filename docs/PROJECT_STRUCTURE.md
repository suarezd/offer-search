# Structure du Projet Offer Search

**Date**: 2025-12-12

Ce document décrit l'organisation complète du projet.

---

## 📁 Vue d'ensemble

```
offer-search/
├── docs/                           # 📚 Documentation
│   ├── adr/                        # Architecture Decision Records
│   ├── guides/                     # Guides utilisateur/développeur
│   ├── HEXAGONAL_ARCHITECTURE_GUIDE.md
│   ├── ARCHITECTURE_IMPLEMENTATION_REPORT.md
│   └── README.md                   # Index documentation
│
├── backend/                        # 🟢 Backend API (Python/FastAPI)
│   ├── app/
│   │   ├── domain/                 # ❤️ Cœur métier
│   │   │   ├── entities/           # Entités métier (Job)
│   │   │   ├── ports/              # Interfaces (IJobRepository)
│   │   │   ├── services/           # Services domaine
│   │   │   └── exceptions/         # Exceptions métier
│   │   ├── application/            # 🎯 Cas d'usage
│   │   │   ├── dto/                # Data Transfer Objects
│   │   │   ├── use_cases/          # Submit, Search, Stats
│   │   │   └── services/           # Services applicatifs
│   │   ├── adapters/
│   │   │   ├── primary/            # 🔵 Entrées (HTTP)
│   │   │   │   └── http/routes/    # Endpoints REST
│   │   │   └── secondary/          # 🟢 Sorties (BDD)
│   │   │       └── persistence/
│   │   │           ├── models/     # SQLAlchemy ORM
│   │   │           ├── database.py # Config BDD
│   │   │           └── sqlalchemy_job_repository.py
│   │   ├── infrastructure/         # ⚙️ Config
│   │   │   └── dependencies.py     # Injection dépendances
│   │   └── main.py                 # Point d'entrée FastAPI
│   ├── tests/                      # Tests (à implémenter)
│   ├── alembic/                    # Migrations BDD
│   ├── requirements.txt            # Dépendances Python
│   └── Dockerfile                  # Image Docker backend
│
├── extension/                      # 🔵 Extension navigateur (TypeScript)
│   ├── src/
│   │   ├── domain/                 # ❤️ Cœur métier
│   │   │   ├── entities/           # Job, JobFilter
│   │   │   └── ports/              # IJobRepository
│   │   ├── application/            # 🎯 Services
│   │   │   └── services/           # JobApplicationService
│   │   ├── adapters/
│   │   │   ├── primary/            # 🔵 UI (Popup, Options)
│   │   │   └── secondary/          # 🟢 Persistence, API
│   │   │       ├── ApiJobRepository.ts
│   │   │       └── LocalJobRepository.ts
│   │   ├── background.ts           # Service worker
│   │   ├── content.ts              # Script injection LinkedIn
│   │   ├── popup/
│   │   │   ├── popup.html
│   │   │   └── popup.ts
│   │   └── manifest.json           # Config extension Chrome
│   ├── public/
│   │   └── icons/                  # Icônes extension
│   ├── dist/                       # Build (généré)
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── docker-compose.yml              # Orchestration containers
├── Makefile                        # Commandes simplifiées
├── README.md                       # Readme principal
└── .gitignore
```

---

## 🏗️ Architecture Backend (Hexagonale)

### Couche Domain (Cœur)

**Responsabilité**: Logique métier pure, sans dépendances externes.

```
backend/app/domain/
├── entities/
│   └── job.py                      # Dataclass Job avec validations
├── ports/
│   └── job_repository.py           # Interface IJobRepository
├── services/
│   └── (vide pour l'instant)
└── exceptions/
    └── job_exceptions.py           # DuplicateJobError, etc.
```

**Règles**:
- ✅ Aucune dépendance FastAPI, SQLAlchemy, etc.
- ✅ Pur Python
- ✅ Testable sans infrastructure

### Couche Application

**Responsabilité**: Orchestration des cas d'usage.

```
backend/app/application/
├── dto/
│   └── job_dto.py                  # Pydantic DTOs
├── use_cases/
│   ├── submit_jobs.py              # Soumission de jobs
│   ├── search_jobs.py              # Recherche
│   └── get_stats.py                # Statistiques
└── services/
    └── (vide pour l'instant)
```

**Flux**: DTO → Use Case → Domain

### Couche Adapters

**Responsabilité**: Interface avec le monde extérieur.

#### Primary (Entrées)

```
backend/app/adapters/primary/http/
└── routes/
    └── job_routes.py               # Endpoints REST API
```

**Flux**: HTTP Request → Route → Use Case

#### Secondary (Sorties)

```
backend/app/adapters/secondary/persistence/
├── models/
│   └── job_model.py                # SQLAlchemy ORM
├── database.py                     # Config async/sync
└── sqlalchemy_job_repository.py    # Implémentation IJobRepository
```

**Flux**: Use Case → IJobRepository → SQLAlchemy → PostgreSQL

### Couche Infrastructure

**Responsabilité**: Configuration et injection de dépendances.

```
backend/app/infrastructure/
└── dependencies.py                 # FastAPI Depends()
```

---

## 🔵 Architecture Frontend (Hexagonale)

### Couche Domain

```
extension/src/domain/
├── entities/
│   ├── Job.ts
│   └── JobFilter.ts
└── ports/
    └── IJobRepository.ts
```

### Couche Application

```
extension/src/application/
└── services/
    └── JobApplicationService.ts
```

### Couche Adapters

```
extension/src/adapters/
├── primary/
│   ├── popup/                      # UI popup
│   └── options/                    # UI options
└── secondary/
    ├── ApiJobRepository.ts         # Fetch API backend
    └── LocalJobRepository.ts       # localStorage
```

---

## 📚 Documentation

```
docs/
├── adr/                            # Architecture Decision Records
│   ├── 000-template.md             # Template ADR
│   ├── 001-hexagonal-architecture-backend.md
│   ├── 002-hexagonal-architecture-frontend.md
│   ├── 003-async-database-operations.md
│   ├── new-adr.sh                  # Script création ADR
│   └── README.md                   # Index ADRs
├── guides/                         # Guides (à créer)
│   ├── backend.md
│   ├── frontend.md
│   └── testing.md
├── HEXAGONAL_ARCHITECTURE_GUIDE.md # Tutoriel complet
├── ARCHITECTURE_IMPLEMENTATION_REPORT.md
├── PROJECT_STRUCTURE.md            # Ce fichier
└── README.md                       # Index documentation
```

---

## 🐳 Infrastructure

### Docker Compose

```yaml
services:
  db:          # PostgreSQL 16
  api:         # Backend FastAPI
  extension-dev: # Frontend dev server
```

### Configuration

- **Backend**: `.env` pour DATABASE_URL
- **Frontend**: `manifest.json` pour permissions

---

## 📦 Dépendances Clés

### Backend (Python)

| Package | Version | Usage |
|---------|---------|-------|
| fastapi | 0.115.5 | Framework web |
| sqlalchemy | 2.0.36 | ORM |
| asyncpg | 0.29.0 | Driver PostgreSQL async |
| pydantic | 2.10.3 | Validation données |
| uvicorn | 0.32.1 | Serveur ASGI |
| alembic | 1.14.0 | Migrations BDD |

### Frontend (TypeScript)

| Package | Version | Usage |
|---------|---------|-------|
| typescript | ^5.x | Langage |
| vite | ^5.x | Build tool |
| @types/chrome | ^0.0.x | Types Chrome API |

---

## 🔄 Flux de Données Complet

```
┌─────────────────┐
│  LinkedIn Page  │
└────────┬────────┘
         │ Scraping (content script)
         ▼
┌─────────────────────────────┐
│  Extension (TypeScript)     │
│  ┌────────────────────────┐ │
│  │  Domain (Job)          │ │
│  └───────────┬────────────┘ │
│              │                │
│  ┌───────────▼────────────┐ │
│  │  Application Service   │ │
│  └───────────┬────────────┘ │
│              │                │
│  ┌───────────▼────────────┐ │
│  │  ApiJobRepository      │ │
│  └───────────┬────────────┘ │
└──────────────┼──────────────┘
               │ HTTP POST /api/jobs/submit
               ▼
┌─────────────────────────────┐
│  Backend API (Python)       │
│  ┌────────────────────────┐ │
│  │  HTTP Routes           │ │
│  └───────────┬────────────┘ │
│              │                │
│  ┌───────────▼────────────┐ │
│  │  SubmitJobsUseCase     │ │
│  └───────────┬────────────┘ │
│              │                │
│  ┌───────────▼────────────┐ │
│  │  Domain (Job entity)   │ │
│  └───────────┬────────────┘ │
│              │                │
│  ┌───────────▼────────────┐ │
│  │  SQLAlchemyRepository  │ │
│  └───────────┬────────────┘ │
└──────────────┼──────────────┘
               │ asyncpg
               ▼
┌─────────────────────────────┐
│  PostgreSQL Database        │
│  Table: jobs                │
└─────────────────────────────┘
```

---

## 📊 Statistiques du Projet

### Backend

| Métrique | Valeur |
|----------|--------|
| Fichiers Python | ~33 |
| Lignes de code | ~1,220 |
| Couches architecture | 4 |
| Endpoints API | 3 |
| Tests | 0 (à implémenter) |

### Frontend

| Métrique | Valeur |
|----------|--------|
| Fichiers TypeScript | ~15 |
| Lignes de code | ~800 |
| Composants UI | 2 (popup, options) |

### Documentation

| Métrique | Valeur |
|----------|--------|
| ADRs | 3 |
| Guides | 3 |
| Pages documentation | 6 |

---

## 🎯 Points d'Entrée Clés

### Backend

- **Main**: `backend/app/main.py`
- **Routes**: `backend/app/adapters/primary/http/routes/job_routes.py`
- **Use Cases**: `backend/app/application/use_cases/`
- **Repository**: `backend/app/adapters/secondary/persistence/sqlalchemy_job_repository.py`

### Frontend

- **Popup**: `extension/src/popup/popup.ts`
- **Background**: `extension/src/background.ts`
- **Content Script**: `extension/src/content.ts`
- **Repository**: `extension/src/adapters/secondary/ApiJobRepository.ts`

---

## 🔗 Liens Utiles

- [Documentation principale](README.md)
- [ADRs](adr/)
- [Guide Architecture Hexagonale](HEXAGONAL_ARCHITECTURE_GUIDE.md)
- [Rapport d'Implémentation](ARCHITECTURE_IMPLEMENTATION_REPORT.md)

---

**Dernière mise à jour**: 2025-12-12
