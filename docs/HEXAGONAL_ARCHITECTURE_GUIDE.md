# Architecture Hexagonale - Backend Offer Search

## Vue d'ensemble

Le backend a été refactoré pour suivre les principes de l'**Architecture Hexagonale** (également appelée Ports & Adapters), permettant une séparation claire des responsabilités et une grande flexibilité pour changer de technologies (base de données, frameworks, etc.).

## Structure du Projet

```
backend/app/
├── domain/                          # ❤️ CŒUR - Logique métier pure
│   ├── entities/
│   │   └── job.py                   # Entité Job (sans dépendances externes)
│   ├── ports/
│   │   └── job_repository.py        # Interface IJobRepository
│   ├── services/
│   │   └── job_domain_service.py    # Services métier
│   └── exceptions/
│       └── job_exceptions.py        # Exceptions métier
│
├── application/                     # 🎯 CAS D'USAGE
│   ├── dto/
│   │   └── job_dto.py              # Data Transfer Objects
│   ├── use_cases/
│   │   ├── submit_jobs.py          # Soumission des jobs
│   │   ├── search_jobs.py          # Recherche des jobs
│   │   └── get_stats.py            # Statistiques
│   └── services/
│       └── job_application_service.py
│
├── adapters/
│   ├── primary/                     # 🔵 ENTRÉES (HTTP, CLI, etc.)
│   │   └── http/
│   │       ├── routes/
│   │       │   └── job_routes.py
│   │       └── dependencies.py
│   │
│   └── secondary/                   # 🟢 SORTIES (BDD, APIs, etc.)
│       └── persistence/
│           ├── sqlalchemy_job_repository.py  # Implémentation PostgreSQL
│           ├── models/
│           │   └── job_model.py    # SQLAlchemy ORM
│           └── database.py
│
├── infrastructure/                  # ⚙️ CONFIGURATION
│   ├── config.py
│   └── dependencies.py              # Injection de dépendances
│
└── main.py                          # Point d'entrée
```

## Les Couches de l'Architecture

### 1. Domain (Cœur métier)

**Responsabilité**: Contient la logique métier pure, sans aucune dépendance externe.

**Fichiers clés**:
- `domain/entities/job.py`: Entité Job avec validations métier
- `domain/ports/job_repository.py`: Interface définissant le contrat du repository
- `domain/exceptions/job_exceptions.py`: Exceptions métier

**Règles**:
- ✅ Aucune dépendance vers les frameworks (FastAPI, SQLAlchemy, etc.)
- ✅ Logique métier pure en Python
- ✅ Facilement testable sans base de données

### 2. Application (Cas d'usage)

**Responsabilité**: Orchestre les cas d'usage en utilisant le domaine.

**Fichiers clés**:
- `application/use_cases/submit_jobs.py`: Logique de soumission de jobs
- `application/use_cases/search_jobs.py`: Logique de recherche
- `application/use_cases/get_stats.py`: Logique de statistiques
- `application/dto/job_dto.py`: Objects de transfert de données

**Règles**:
- ✅ Utilise les ports du domaine
- ✅ Ne dépend pas des adapters
- ✅ Coordonne les opérations métier

### 3. Adapters (Adaptateurs)

#### 3.1 Primary Adapters (Entrées)

**Responsabilité**: Exposent l'application au monde extérieur (HTTP, CLI, etc.).

**Fichiers clés**:
- `adapters/primary/http/routes/job_routes.py`: Endpoints REST API

**Flux**:
```
HTTP Request → Route Handler → Use Case → Domain
```

#### 3.2 Secondary Adapters (Sorties)

**Responsabilité**: Implémentent les ports définis par le domaine (base de données, APIs externes, etc.).

**Fichiers clés**:
- `adapters/secondary/persistence/sqlalchemy_job_repository.py`: Implémentation PostgreSQL
- `adapters/secondary/persistence/models/job_model.py`: Modèle ORM SQLAlchemy
- `adapters/secondary/persistence/database.py`: Configuration base de données

**Flux**:
```
Use Case → IJobRepository (port) → SQLAlchemyJobRepository (adapter) → PostgreSQL
```

### 4. Infrastructure

**Responsabilité**: Configuration et injection de dépendances.

**Fichiers clés**:
- `infrastructure/dependencies.py`: Injection de dépendances FastAPI

## Flux de Données

### Exemple: Recherche de Jobs

```
┌─────────────┐
│   Client    │
└─────┬───────┘
      │ POST /api/jobs/search
      ▼
┌─────────────────────────────┐
│  Primary Adapter (HTTP)     │
│  job_routes.py              │
└─────┬───────────────────────┘
      │ Depends(get_search_jobs_use_case)
      ▼
┌─────────────────────────────┐
│  Infrastructure             │
│  dependencies.py            │
└─────┬───────────────────────┘
      │ Creates SearchJobsUseCase
      ▼
┌─────────────────────────────┐
│  Application Layer          │
│  SearchJobsUseCase          │
└─────┬───────────────────────┘
      │ use_case.execute(filter_dto)
      ▼
┌─────────────────────────────┐
│  Domain Port                │
│  IJobRepository.search()    │
└─────┬───────────────────────┘
      │ Implemented by
      ▼
┌─────────────────────────────┐
│  Secondary Adapter          │
│  SQLAlchemyJobRepository    │
└─────┬───────────────────────┘
      │ SQLAlchemy queries
      ▼
┌─────────────────────────────┐
│  PostgreSQL Database        │
└─────────────────────────────┘
```

## Avantages de cette Architecture

### 1. **Changement de Base de Données Facilité**

Pour changer de PostgreSQL vers MongoDB, il suffit de :
1. Créer `MongoJobRepository` qui implémente `IJobRepository`
2. Modifier `infrastructure/dependencies.py` pour injecter le nouveau repository

```python
# Avant
return SQLAlchemyJobRepository(session)

# Après
return MongoJobRepository(mongo_client)
```

**Aucun changement** dans le domaine ou les use cases !

### 2. **Testabilité**

Vous pouvez tester la logique métier sans base de données :

```python
# Test avec mock repository
mock_repo = Mock(spec=IJobRepository)
use_case = SearchJobsUseCase(mock_repo)
result = await use_case.execute(filter_dto)
```

### 3. **Évolutivité**

Ajouter de nouvelles sources de données (Indeed, Monster, etc.) est trivial :
- Créer un nouveau scraper
- Utiliser le même `SubmitJobsUseCase`
- Pas de modification du domaine

### 4. **Indépendance des Frameworks**

Le domaine ne dépend ni de FastAPI, ni de SQLAlchemy, ni d'aucun framework.

### 5. **Cohérence avec le Frontend**

Le frontend utilise également l'architecture hexagonale, créant une cohérence sur tout le projet.

## Endpoints API

### 1. POST /api/jobs/submit

Soumet de nouveaux jobs avec détection des doublons.

**Request**:
```json
{
  "jobs": [{
    "id": "job-123",
    "title": "Développeur Python",
    "company": "Tech Corp",
    "location": "Paris",
    "url": "https://example.com/job",
    "source": "linkedin",
    "posted_date": "2025-12-10",
    "description": "Description du poste",
    "scraped_at": "2025-12-12T10:00:00"
  }]
}
```

**Response**:
```json
{
  "success": true,
  "inserted": 1,
  "duplicates": 0,
  "total": 1
}
```

### 2. POST /api/jobs/search

Recherche de jobs avec filtres.

**Request**:
```json
{
  "search": "Python",
  "location": "Paris",
  "company": "Tech",
  "source": "linkedin",
  "limit": 50,
  "offset": 0
}
```

**Response**:
```json
[{
  "id": "job-123",
  "title": "Développeur Python",
  "company": "Tech Corp",
  "location": "Paris",
  "url": "https://example.com/job",
  "source": "linkedin",
  "posted_date": "2025-12-10",
  "description": "Description",
  "scraped_at": "2025-12-12T10:00:00Z",
  "created_at": "2025-12-12T10:18:06Z",
  "updated_at": null
}]
```

### 3. GET /api/jobs/stats

Statistiques sur les jobs.

**Response**:
```json
{
  "total_jobs": 150,
  "total_companies": 45,
  "total_locations": 23,
  "jobs_by_source": {
    "linkedin": 150
  }
}
```

## Migration vers MongoDB (Exemple)

Voici comment créer un adapter MongoDB :

```python
# adapters/secondary/persistence/mongo_job_repository.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.domain.ports.job_repository import IJobRepository

class MongoJobRepository(IJobRepository):
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client.offer_search
        self.collection = self.db.jobs

    async def save(self, job: Job) -> Job:
        document = {
            "_id": job.id,
            "title": job.title,
            "company": job.company,
            # ... autres champs
        }
        await self.collection.insert_one(document)
        return job

    # Implémenter les autres méthodes...
```

Puis dans `infrastructure/dependencies.py` :

```python
from motor.motor_asyncio import AsyncIOMotorClient

async def get_job_repository() -> IJobRepository:
    mongo_client = AsyncIOMotorClient(MONGO_URL)
    return MongoJobRepository(mongo_client)
```

**C'est tout !** Aucune modification du domaine, des use cases ou des routes HTTP nécessaire.

## Technologies Utilisées

- **FastAPI**: Framework web asynchrone
- **SQLAlchemy 2.0**: ORM avec support async
- **asyncpg**: Driver PostgreSQL asynchrone
- **Pydantic**: Validation des données
- **PostgreSQL 16**: Base de données (facilement remplaçable)

## Tests

Pour tester l'architecture :

```bash
# Tester les endpoints
curl http://localhost:8000/api/jobs/stats
curl -X POST http://localhost:8000/api/jobs/search -H "Content-Type: application/json" -d '{"limit": 10}'

# Tester la soumission
curl -X POST http://localhost:8000/api/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{"jobs": [{"id": "test", "title": "Dev", "company": "Co", "location": "Paris", "url": "http://ex.com", "source": "linkedin", "scraped_at": "2025-12-12T10:00:00"}]}'
```

## Prochaines Étapes

1. **Tests Unitaires**: Ajouter des tests pour le domaine et les use cases
2. **Tests d'Intégration**: Tester les adapters avec une vraie base de données
3. **Documentation API**: Générer documentation OpenAPI/Swagger
4. **Monitoring**: Ajouter logs et métriques
5. **Cache**: Ajouter un adapter Redis pour le cache

## Conclusion

L'architecture hexagonale rend le backend :
- ✅ **Flexible**: Changement de BDD en quelques lignes
- ✅ **Testable**: Logique métier testable sans infrastructure
- ✅ **Maintenable**: Séparation claire des responsabilités
- ✅ **Évolutif**: Facile d'ajouter de nouvelles fonctionnalités
- ✅ **Professionnel**: Architecture moderne et reconnue
