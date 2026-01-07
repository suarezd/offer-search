# Architecture Decision Records - Vue d'ensemble

Ce document consolide les décisions architecturales et la documentation technique du projet Offer Search.

## 📋 Table des matières

- [Architecture Hexagonale](#architecture-hexagonale)
- [Structure du Projet](#structure-du-projet)
- [Implémentation et Migration](#implémentation-et-migration)
- [ADRs Spécifiques](#adrs-spécifiques)

---

## Architecture Hexagonale

Le projet Offer Search utilise l'architecture hexagonale (Ports & Adapters) pour garantir la séparation des préoccupations et la testabilité.

### Principes fondamentaux

```
┌─────────────────────────────────────────┐
│        PRIMARY ADAPTERS                 │
│      (HTTP Routes, UI)                  │
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
│       SECONDARY ADAPTERS                │
│   (PostgreSQL, External APIs)           │
└─────────────────────────────────────────┘
```

### Couches de l'architecture

1. **Domain** (Cœur métier)
   - Entités métier (`Job`, etc.)
   - Ports (interfaces) : `IJobRepository`
   - Exceptions métier : `DuplicateJobError`, `JobNotFoundError`
   - Logique métier pure, **indépendante** des frameworks

2. **Application** (Orchestration)
   - Use Cases : `SubmitJobsUseCase`, `SearchJobsUseCase`
   - DTOs : `JobCreateDTO`, `JobResponseDTO`
   - Services applicatifs

3. **Adapters** (Interface monde extérieur)
   - **Primary** : HTTP Routes (FastAPI), UI (Extension Chrome)
   - **Secondary** : PostgreSQL Repository, APIs externes

4. **Infrastructure** (Configuration)
   - Dependency Injection (FastAPI)
   - Configuration base de données
   - Configuration frameworks

### Avantages

- ✅ **Testabilité** : Le domaine peut être testé sans frameworks
- ✅ **Maintenabilité** : Changement de BDD/framework sans toucher au métier
- ✅ **Indépendance** : Le domaine ne dépend de rien
- ✅ **Flexibilité** : Facile d'ajouter de nouveaux adapters

### Exemples d'implémentation

#### Backend (Python/FastAPI)

```
backend/app/
├── domain/                          # ❤️ Cœur métier
│   ├── entities/job.py             # Entité Job
│   ├── ports/job_repository.py     # Interface IJobRepository
│   └── exceptions/job_exceptions.py
├── application/                     # 🎯 Use Cases (CQRS)
│   ├── commands/                   # SubmitJobsCommand
│   ├── queries/                    # SearchJobsQuery, GetStatsQuery
│   └── dto/job_dto.py
├── infrastructure/                  # 🔌 Infrastructure
│   ├── http/                       # Routes HTTP
│   ├── persistence/                # PostgreSQL Repository
│   └── dependencies.py             # Configuration DI
```

#### Frontend (TypeScript/Extension Chrome)

```
src/
├── domain/                    # Cœur métier
│   ├── entities/
│   └── ports/                # IJobRepository, IJobScraper
├── application/              # Use Cases (CQRS)
│   ├── commands/             # ScrapeJobsCommand, SubmitJobsCommand
│   └── queries/              # SearchJobsQuery, GetStatsQuery
└── infrastructure/           # Infrastructure
    ├── ui/                   # Interface utilisateur (Popup)
    └── api/                  # Communication réseau (Repository, Scrapers)
```

---

## Structure du Projet

### Vue d'ensemble

```
offer-search/
├── backend/                    # 🟢 Backend API (Python/FastAPI)
│   ├── app/
│   │   ├── domain/            # ❤️ Cœur métier
│   │   ├── application/       # 🎯 Use cases
│   │   ├── adapters/          # 🔌 HTTP + PostgreSQL
│   │   └── infrastructure/    # ⚙️ Configuration
│   ├── tests/                 # 88 tests (unitaires, intégration, E2E)
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── functional/
│   │   └── e2e/
│   ├── Dockerfile
│   └── requirements.txt
│
├── extension/                  # 🔵 Extension navigateur (TypeScript)
│   ├── src/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── adapters/
│   │   ├── background.ts
│   │   ├── content.ts
│   │   └── popup/
│   ├── dist/                  # Build (généré)
│   └── manifest.json
│
├── docs/                       # 📚 Documentation
│   ├── adr/                   # Architecture Decision Records
│   │   ├── ADR.md            # ⭐ Ce fichier
│   │   ├── 001-hexagonal-architecture-backend.md
│   │   ├── 002-hexagonal-architecture-frontend.md
│   │   └── 003-async-database-operations.md
│   └── README.md
│
├── .github/workflows/          # CI/CD
│   └── tests.yml
│
├── docker-compose.yml          # 🐳 Orchestration
├── Makefile                    # 🛠️ Commandes
├── README.md                   # Documentation principale
├── QUICK_START.md             # Guide de démarrage
├── TESTING.md                 # Guide des tests
└── CHANGELOG.md               # Historique
```

### Technologies utilisées

#### Backend
- **Python 3.11** - Langage
- **FastAPI** - Framework web moderne et rapide
- **PostgreSQL 16** - Base de données relationnelle
- **SQLAlchemy 2.0** - ORM avec support async
- **asyncpg** - Driver PostgreSQL async (+60% performance vs psycopg2)
- **Pydantic** - Validation de données
- **pytest** - Tests (88 tests : unitaires, intégration, E2E)
- **Docker** - Conteneurisation

#### Frontend
- **TypeScript** - Langage typé
- **Vite** - Build tool rapide
- **Chrome Extension Manifest V3** - API extension moderne
- **Architecture hexagonale** - Organisation du code

#### Infrastructure
- **Docker Compose** - Orchestration des services
- **Selenium Grid** - Tests E2E cross-platform
- **GitHub Actions** - CI/CD automatisé
- **Make** - Automatisation des commandes

---

## Implémentation et Migration

### Historique du projet

Le projet a évolué à travers plusieurs phases architecturales :

**Phase 1 : POC Simple**
- Extension Chrome basique
- Scraping LinkedIn sans backend
- Stockage local uniquement

**Phase 2 : Backend Centralisé**
- Ajout d'une API FastAPI
- Base de données PostgreSQL
- Architecture monolithique

**Phase 3 : Architecture Hexagonale (Actuelle)**
- Refactoring complet backend → architecture hexagonale
- Refactoring frontend → architecture hexagonale
- Tests exhaustifs (88 tests)
- Support async avec asyncpg (+60% performance)

### Migration vers l'architecture hexagonale

#### Backend

**Avant (Architecture classique)**
```python
# routes.py (tout mélangé)
@app.post("/jobs")
def create_job(job_data: dict):
    # Validation mélangée avec logique métier
    # Accès direct à SQLAlchemy
    # Pas de séparation des responsabilités
```

**Après (Architecture hexagonale)**
```python
# adapters/primary/http/routes/job_routes.py
@router.post("/api/jobs/submit")
async def submit_jobs(request: SubmitJobsRequest):
    use_case = SubmitJobsUseCase(job_repository)
    return await use_case.execute(request)

# application/use_cases/submit_jobs.py
class SubmitJobsUseCase:
    def __init__(self, job_repository: IJobRepository):
        self._repository = job_repository

    async def execute(self, request):
        jobs = [Job.from_dto(dto) for dto in request.jobs]
        return await self._repository.save_jobs(jobs)

# domain/entities/job.py
@dataclass
class Job:
    id: str
    title: str
    # ... logique métier pure
```

#### Avantages constatés

- ✅ **+300% de tests** : 20 tests → 88 tests
- ✅ **+60% de performance** : Migration vers asyncpg
- ✅ **100% du domaine testable** : Sans dépendances externes
- ✅ **Maintenance facilitée** : Séparation claire des responsabilités
- ✅ **Évolutivité** : Facile d'ajouter de nouveaux features

### Base de données

#### Modèle Job

| Champ | Type | Description |
|-------|------|-------------|
| id | String(50) PK | ID unique LinkedIn |
| title | String(255) | Titre du poste |
| company | String(255) | Nom entreprise |
| location | String(255) | Localisation |
| url | String(500) | URL offre |
| posted_date | String(100) | Date publication |
| description | Text | Description complète |
| scraped_at | DateTime | Date de scraping |
| created_at | DateTime | Date création DB |
| updated_at | DateTime | Date MAJ |

#### Index
- `idx_title_company` : (title, company) - Recherche par titre/entreprise
- `idx_location_company` : (location, company) - Recherche par localisation

#### Performance async
Passage de `psycopg2` à `asyncpg` :
- **Avant** : ~1500 ms pour 100 insertions
- **Après** : ~600 ms pour 100 insertions
- **Gain** : +60% de performance

---

## ADRs Spécifiques

Ce projet suit le format ADR (Architecture Decision Records) pour documenter les décisions architecturales importantes.

### Liste des ADRs

1. **[ADR-001 : Architecture Hexagonale Backend](001-hexagonal-architecture-backend.md)**
   - Décision : Adopter l'architecture hexagonale pour le backend
   - Statut : Accepté et implémenté
   - Impact : Séparation Domain/Application/Adapters/Infrastructure

2. **[ADR-002 : Architecture Hexagonale Frontend](002-hexagonal-architecture-frontend.md)**
   - Décision : Appliquer l'architecture hexagonale à l'extension Chrome
   - Statut : Accepté et implémenté
   - Impact : Extension structurée en couches

3. **[ADR-003 : Opérations Asynchrones Base de Données](003-async-database-operations.md)**
   - Décision : Utiliser asyncpg au lieu de psycopg2
   - Statut : Accepté et implémenté
   - Impact : +60% de performance, meilleure scalabilité

4. **[ADR-004 : CQRS Simple pour le Frontend](004-cqrs-simple-frontend.md)**
   - Décision : Adopter le pattern CQRS simple pour séparer Commands et Queries
   - Statut : Accepté et implémenté
   - Impact : Meilleure clarté architecturale, maintenabilité améliorée

5. **[ADR-005 : CQRS Simple pour le Backend](005-cqrs-simple-backend.md)**
   - Décision : Adopter CQRS simple et simplifier la nomenclature infrastructure
   - Statut : Accepté et implémenté
   - Impact : Cohérence totale frontend/backend, nomenclature claire

6. **[ADR-006 : Intégration du scraper Indeed](006-integration-indeed-scraper.md)**
   - Décision : Ajouter Indeed comme source de jobs aux côtés de LinkedIn
   - Statut : Accepté et implémenté
   - Impact : Extension multi-sources, démonstration de l'extensibilité de l'architecture

### Template ADR

Pour créer un nouvel ADR, utilisez le template : [000-template.md](000-template.md)

---

## Ressources

### Documentation projet
- [README principal](../../README.md)
- [Guide de démarrage rapide](../../QUICK_START.md)
- [Guide des tests](../../TESTING.md)
- [Changelog](../../CHANGELOG.md)

### Documentation externe
- [Architecture Hexagonale (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

**Dernière mise à jour** : 2026-01-07
**Mainteneurs** : @suarezd
