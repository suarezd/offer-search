# ADR-005: Adoption du pattern CQRS simple pour le backend

**Date**: 2026-01-07

**Auteurs**: Diego, Claude

**Statut**: ✅ **Accepté**

---

## Contexte

Le backend Python utilisait déjà une architecture hexagonale avec des use cases bien séparés (`SubmitJobsUseCase`, `SearchJobsUseCase`, `GetStatsUseCase`), mais la structure présentait des incohérences avec le frontend et utilisait une nomenclature peu claire.

### Problématiques identifiées

1. **Nomenclature infrastructure peu claire**
   - `infrastructure/primary/` et `infrastructure/secondary/` : jargon hexagonal peu accessible
   - Incohérence avec le frontend qui utilise `infrastructure/ui/` et `infrastructure/api/`

2. **Pas de distinction explicite Commands vs Queries**
   - Les use cases étaient dans un seul répertoire `use_cases/`
   - Difficile de distinguer les opérations de lecture vs écriture
   - Manque de clarté sur la responsabilité de chaque use case

3. **Incohérence frontend/backend**
   - Frontend : `application/commands/` et `application/queries/`
   - Backend : `application/use_cases/`
   - Vocabulaire différent entre les deux parties du projet

---

## Décision

Adoption du **pattern CQRS simple** pour aligner le backend sur la même architecture que le frontend, avec refactoring de l'infrastructure pour améliorer la clarté.

### Structure implémentée

```python
backend/app/
├── domain/
│   ├── entities/
│   │   └── job.py                       ✅ Entité Job
│   ├── ports/
│   │   └── job_repository.py            ✅ Interface IJobRepository
│   └── exceptions/
│       └── job_exceptions.py            ✅ Exceptions métier
├── application/
│   ├── commands/                        🆕 CQRS - Modifications d'état
│   │   └── submit_jobs_command.py       (ex SubmitJobsUseCase)
│   ├── queries/                         🆕 CQRS - Lectures seules
│   │   ├── search_jobs_query.py         (ex SearchJobsUseCase)
│   │   └── get_stats_query.py           (ex GetStatsUseCase)
│   └── dto/
│       └── job_dto.py                   ✅ DTOs
└── infrastructure/
    ├── http/                            🔄 ex primary/http
    │   └── routes/
    │       └── job_routes.py
    ├── persistence/                     🔄 ex secondary/persistence
    │   ├── database.py
    │   ├── models/
    │   │   └── job_model.py
    │   └── sqlalchemy_job_repository.py
    └── dependencies.py                  ✅ Configuration DI
```

### Principes appliqués

1. **Séparation Command/Query explicite**
   - Commands modifient l'état (`SubmitJobsCommand`)
   - Queries lisent l'état (`SearchJobsQuery`, `GetStatsQuery`)

2. **Nomenclature cohérente avec le frontend**
   - Backend `http/` ↔ Frontend `ui/`
   - Backend `persistence/` ↔ Frontend `api/`
   - Commands et Queries des deux côtés

3. **Simplification de la structure**
   - Suppression des niveaux `primary/` et `secondary/`
   - `infrastructure/http/` plus clair que `infrastructure/primary/http/`
   - `infrastructure/persistence/` plus explicite que `infrastructure/secondary/persistence/`

---

## Conséquences

### ✅ Avantages

1. **Cohérence frontend/backend totale**
   - Même vocabulaire (Commands, Queries)
   - Même organisation (application/commands/, application/queries/)
   - Facilite l'onboarding et la maintenance

2. **Clarté architecturale améliorée**
   - Distinction explicite lecture vs écriture
   - Intention claire dans le nom des classes
   - `http/` et `persistence/` plus parlants que `primary/` et `secondary/`

3. **Maintenabilité**
   - Structure plus plate, moins de niveaux de répertoires
   - Imports plus courts et plus clairs
   - Facile de localiser un use case

4. **Scalabilité**
   - Prépare l'ajout de nouveaux commands (DeleteJobCommand, UpdateJobCommand)
   - Prépare l'ajout de nouvelles queries (GetJobByIdQuery, SearchByDateQuery)
   - Base saine pour CQRS avancé si besoin futur

5. **Testabilité**
   - Aucun changement dans les tests grâce aux ports
   - Les 67 tests continuent de passer sans modification de logique
   - Seuls les imports ont été adaptés

### ⚠️ Inconvénients

1. **Migration initiale**
   - Renommage de tous les use cases
   - Adaptation de tous les imports
   - Mise à jour de la documentation

2. **Légère verbosité**
   - `SubmitJobsCommand` vs `SubmitJobsUseCase`
   - Mais gain en clarté et intention explicite

---

## Alternatives considérées

### 1. Garder use_cases/ avec nomenclature primary/secondary

**Pour**:
- Pas de migration nécessaire
- Code déjà fonctionnel

**Contre**:
- Incohérence avec le frontend
- Nomenclature `primary/secondary` peu accessible
- Manque de distinction Commands vs Queries

**Verdict**: ❌ Pas durable, dette technique

### 2. CQRS avancé avec Event Sourcing

**Pour**:
- Historique complet des modifications
- Audit trail
- Scalabilité maximale

**Contre**:
- Overkill pour le projet actuel
- Complexité excessive
- Overhead de stockage important

**Verdict**: ❌ Trop complexe

### 3. Garder CQRS mais conserver primary/secondary

**Pour**:
- Adoption partielle de CQRS
- Moins de changements

**Contre**:
- Incohérence partielle avec frontend
- Toujours la problématique de nomenclature

**Verdict**: ⚖️ Mieux mais incomplet

---

## Implémentation

### Commands créés

**SubmitJobsCommand** (65 lignes)
```python
class SubmitJobsCommand:
    """Command pour soumettre des jobs à la base de données."""

    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self, jobs_dto: List[JobCreateDTO]) -> Dict[str, Any]:
        # Validation et création des entités Job
        # Persistance via repository
        # Retour du résultat
```

### Queries créées

**SearchJobsQuery** (47 lignes)
```python
class SearchJobsQuery:
    """Query pour rechercher des jobs selon des critères."""

    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self, filter_dto: JobFilterDTO) -> List[Job]:
        # Validation des critères
        # Recherche via repository
        # Retour des résultats
```

**GetStatsQuery** (35 lignes)
```python
class GetStatsQuery:
    """Query pour récupérer les statistiques des jobs."""

    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self) -> JobStatsDTO:
        # Agrégation via repository
        # Construction du DTO de statistiques
        # Retour
```

### Refactoring infrastructure

**Avant**:
```
infrastructure/
├── primary/
│   └── http/
│       └── routes/job_routes.py
└── secondary/
    └── persistence/
        ├── database.py
        ├── models/job_model.py
        └── sqlalchemy_job_repository.py
```

**Après**:
```
infrastructure/
├── http/
│   └── routes/job_routes.py
├── persistence/
│   ├── database.py
│   ├── models/job_model.py
│   └── sqlalchemy_job_repository.py
└── dependencies.py
```

### Adaptation des routes

**Avant**:
```python
from app.application.use_cases.submit_jobs import SubmitJobsUseCase
from app.infrastructure.dependencies import get_submit_jobs_use_case

@router.post("/submit")
async def submit_jobs(
    request: JobsSubmitRequestDTO,
    use_case: SubmitJobsUseCase = Depends(get_submit_jobs_use_case)
):
    result = await use_case.execute(request.jobs)
```

**Après**:
```python
from app.application.commands.submit_jobs_command import SubmitJobsCommand
from app.infrastructure.dependencies import get_submit_jobs_command

@router.post("/submit")
async def submit_jobs(
    request: JobsSubmitRequestDTO,
    command: SubmitJobsCommand = Depends(get_submit_jobs_command)
):
    result = await command.execute(request.jobs)
```

### Fichiers impactés

**Créés**:
- `app/application/commands/submit_jobs_command.py`
- `app/application/queries/search_jobs_query.py`
- `app/application/queries/get_stats_query.py`

**Modifiés**:
- `app/infrastructure/http/routes/job_routes.py` (imports et noms)
- `app/infrastructure/dependencies.py` (factory functions)
- `app/main.py` (imports infrastructure)
- `app/infrastructure/persistence/models/job_model.py` (imports)
- `app/infrastructure/persistence/sqlalchemy_job_repository.py` (imports)
- Tous les tests (imports uniquement)

**Supprimés**:
- `app/application/use_cases/submit_jobs.py`
- `app/application/use_cases/search_jobs.py`
- `app/application/use_cases/get_stats.py`
- `app/infrastructure/primary/` (répertoire)
- `app/infrastructure/secondary/` (répertoire)

---

## Validation

### Tests

✅ **67 tests passent** :
- 36 tests unitaires (domain)
- 20 tests d'intégration (repository)
- 11 tests fonctionnels BDD (use cases)

```bash
$ make test-all
Running unit tests...
============================== 36 passed in 0.05s ==============================
Running integration tests...
============================== 20 passed in 0.73s ==============================
Running functional/BDD tests...
============================== 11 passed in 0.04s ==============================
All backend tests passed!
```

### Structure finale

```
backend/app/
├── application/
│   ├── commands/     (1 fichier)
│   ├── queries/      (2 fichiers)
│   └── dto/          (1 fichier)
├── domain/
│   ├── entities/     (1 fichier)
│   ├── ports/        (1 fichier)
│   └── exceptions/   (1 fichier)
└── infrastructure/
    ├── http/         (1 fichier routes)
    ├── persistence/  (3 fichiers)
    └── dependencies.py

Total: 26 fichiers Python (structure clean et plate)
```

---

## Impact sur l'architecture

### Aucun changement dans le domain ✅

- `domain/entities/job.py` : inchangé
- `domain/ports/job_repository.py` : inchangé
- `domain/exceptions/` : inchangé

Le domain reste pur et indépendant, conformément à l'architecture hexagonale.

### Aucun changement dans la persistence ✅

- `SQLAlchemyJobRepository` : inchangé (implémente toujours `IJobRepository`)
- `JobModel` : inchangé
- `database.py` : inchangé

Seuls les imports ont été adaptés (`secondary.persistence` → `persistence`).

### Changements uniquement dans application et nomenclature

- Application : use_cases → commands + queries
- Infrastructure : primary/secondary → http/persistence

---

## Cohérence Frontend/Backend

### Comparaison des structures

| Frontend (TypeScript) | Backend (Python) |
|----------------------|------------------|
| `domain/entities/Job.ts` | `domain/entities/job.py` |
| `domain/ports/IJobRepository.ts` | `domain/ports/job_repository.py` |
| `application/commands/` | `application/commands/` |
| `application/queries/` | `application/queries/` |
| `infrastructure/ui/` | `infrastructure/http/` |
| `infrastructure/api/` | `infrastructure/persistence/` |

### Vocabulaire unifié

| Concept | Frontend | Backend |
|---------|----------|---------|
| Modification d'état | `ScrapeJobsCommand` | `SubmitJobsCommand` |
| Lecture seule | `SearchJobsQuery` | `SearchJobsQuery` |
| Interface utilisateur | `infrastructure/ui/` | `infrastructure/http/` |
| Accès données | `infrastructure/api/` | `infrastructure/persistence/` |

---

## Références

- [ADR-004](004-cqrs-simple-frontend.md) - CQRS Simple pour le Frontend (cohérence)
- [ADR-001](001-hexagonal-architecture-backend.md) - Architecture Hexagonale Backend (base)
- [Martin Fowler - CQRS](https://martinfowler.com/bliki/CQRS.html)
- Code source: [backend/app/](../../backend/app/)

---

## Prochaines étapes

1. ⏳ Monitorer la facilité d'ajout de nouveaux commands/queries
2. ⏳ Évaluer si des optimisations de cache sont nécessaires sur les Queries
3. ⏳ Considérer l'ajout de nouveaux commands (DeleteJob, UpdateJob)
4. ⏳ Documenter les patterns d'utilisation pour les contributeurs

---

## Risques et Mitigations

### Risque 1: Confusion avec les anciens chemins

**Impact**: Faible
**Probabilité**: Moyenne
**Mitigation**:
- Tous les imports ont été adaptés automatiquement
- Tous les tests passent
- Documentation mise à jour
- Anciens répertoires supprimés

### Risque 2: Régression sur la CI GitHub

**Impact**: Élevé
**Probabilité**: Faible
**Mitigation**:
- Tests locaux passent tous (67/67)
- CI utilise pytest qui utilise les nouveaux imports
- Aucun changement nécessaire dans `.github/workflows/tests.yml`

---

## Notes

Cette refonte améliore significativement la cohérence du projet en alignant parfaitement le backend sur le frontend. La migration a été réalisée sans aucune régression (tous les tests passent) grâce à l'architecture hexagonale qui isole bien le domain de l'infrastructure.

Le pattern CQRS simple est un excellent équilibre entre clarté architecturale et simplicité d'implémentation.

---

## Changelog

- **2026-01-07**: Création de l'ADR
- **2026-01-07**: Implémentation complète et validation (67 tests passent)
- **2026-01-07**: Statut changé à Accepté

---

**Dernière révision**: 2026-01-07
