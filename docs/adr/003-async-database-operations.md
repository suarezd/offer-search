# ADR-003: Utilisation d'asyncpg pour les opérations asynchrones

**Date**: 2025-12-12

**Auteurs**: Diego, Claude Sonnet 4.5

**Statut**: ✅ **Accepté**

---

## Contexte

Lors de l'implémentation de l'architecture hexagonale (ADR-001), nous avons identifié le besoin de support asynchrone pour :
- Améliorer les performances du backend
- Gérer les requêtes concurrentes efficacement
- Exploiter pleinement FastAPI (framework async)
- Préparer la scalabilité future

### État initial

Le backend utilisait :
- **psycopg2-binary**: Driver PostgreSQL synchrone
- **SQLAlchemy** sans async
- Opérations bloquantes sur les I/O database

### Problèmes identifiés

1. **Performance**: Requêtes synchrones bloquant l'event loop FastAPI
2. **Concurrence limitée**: Chaque requête bloque un thread
3. **Scalabilité**: Difficulté à gérer >100 req/s
4. **Non-idiomatic**: FastAPI est conçu pour async/await

---

## Décision

Adoption d'**asyncpg** comme driver PostgreSQL asynchrone, avec :

1. **SQLAlchemy 2.0+ avec support async**
   - `create_async_engine()` pour connexions async
   - `AsyncSession` pour les transactions
   - `async_sessionmaker` pour le pool

2. **asyncpg** comme driver sous-jacent
   - Driver PostgreSQL natif async
   - Performance supérieure à psycopg2
   - Support complet des fonctionnalités PostgreSQL

3. **Coexistence sync/async**
   - psycopg2 conservé pour Alembic (migrations)
   - asyncpg pour l'application runtime
   - Deux engines distincts

### Configuration

```python
# Async (application)
ASYNC_DATABASE_URL = "postgresql+asyncpg://user:pass@host:port/db"
async_engine = create_async_engine(ASYNC_DATABASE_URL)

# Sync (migrations Alembic)
DATABASE_URL = "postgresql://user:pass@host:port/db"
engine = create_engine(DATABASE_URL)
```

---

## Conséquences

### ✅ Avantages

1. **Performance**
   - Requêtes non-bloquantes
   - Event loop FastAPI pleinement exploité
   - Latence réduite sur charges concurrentes

2. **Scalabilité**
   - Gestion de milliers de connexions concurrentes
   - Utilisation CPU/RAM optimisée
   - Prêt pour load balancing

3. **Cohérence avec FastAPI**
   - Endpoints async de bout en bout
   - `async def` partout dans le code
   - Idiomatic Python moderne

4. **Prêt pour le futur**
   - Support WebSockets facile
   - Streaming de données possible
   - Micro-services async

### ⚠️ Inconvénients

1. **Complexité**
   - Gestion de deux drivers (asyncpg + psycopg2)
   - Deux configurations de connexion
   - Courbe d'apprentissage async/await

2. **Compatibilité**
   - Alembic nécessite psycopg2 (sync)
   - Certains outils nécessitent connexions sync
   - Migration plus délicate

3. **Debugging**
   - Stack traces async plus complexes
   - Outils de profiling à adapter

---

## Alternatives considérées

### 1. Garder psycopg2 (synchrone)

**Pour**:
- Simple et éprouvé
- Pas de migration nécessaire
- Alembic fonctionne directement

**Contre**:
- Performance limitée
- Bloque l'event loop FastAPI
- Non-scalable

**Verdict**: ❌ Ne convient pas pour async

### 2. psycopg3 avec mode async

**Pour**:
- Nouvelle version de psycopg
- Support async natif
- API familière

**Contre**:
- Moins mature qu'asyncpg
- Performance inférieure
- Moins d'adoption communautaire

**Verdict**: ⚖️ Bon choix mais moins performant

### 3. Utiliser un ORM full async (Tortoise ORM, Prisma)

**Pour**:
- ORM conçu pour async
- API moderne
- Pas de double configuration

**Contre**:
- Migration complète nécessaire
- Écosystème moins mature
- SQLAlchemy plus flexible

**Verdict**: ❌ Trop de changements

---

## Implémentation

### Fichiers modifiés

1. **requirements.txt**
   ```diff
   + asyncpg==0.29.0
   ```

2. **database.py**
   ```python
   # Async engine
   ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
   async_engine = create_async_engine(ASYNC_DATABASE_URL)
   AsyncSessionLocal = async_sessionmaker(async_engine, ...)
   ```

3. **sqlalchemy_job_repository.py**
   ```python
   class SQLAlchemyJobRepository(IJobRepository):
       def __init__(self, session: AsyncSession):
           self.session = session

       async def search(...):
           stmt = select(JobModel).where(...)
           result = await self.session.execute(stmt)
           return result.scalars().all()
   ```

4. **dependencies.py**
   ```python
   async def get_async_db():
       async with AsyncSessionLocal() as session:
           yield session
   ```

### Migration

- ✅ Tous les repositories convertis en async
- ✅ Tous les use cases en async
- ✅ Toutes les routes en async
- ✅ Tests fonctionnels passés

---

## Performance

### Benchmarks (estimés)

| Métrique | Sync (psycopg2) | Async (asyncpg) | Gain |
|----------|-----------------|-----------------|------|
| Latence p50 | ~50ms | ~20ms | -60% |
| Latence p99 | ~200ms | ~80ms | -60% |
| Throughput | ~100 req/s | ~500 req/s | +400% |
| Connexions max | ~200 | ~2000 | +900% |

> **Note**: Benchmarks à valider avec tests de charge réels

---

## Validation

### Tests effectués

✅ Insertion de jobs (async)
✅ Recherche de jobs (async)
✅ Statistiques (async)
✅ Requêtes concurrentes (10 simultanées)
✅ Alembic migrations (sync toujours fonctionnel)

### Build & Déploiement

✅ Docker build réussi
✅ Container démarré sans erreurs
✅ Tous les endpoints fonctionnels

---

## Dépendances

### Avant
```txt
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
```

### Après
```txt
sqlalchemy==2.0.36
psycopg2-binary==2.9.10  # Conservé pour Alembic
asyncpg==0.29.0          # Nouveau pour async
```

---

## Références

- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [FastAPI Async SQL](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- [ADR-001](001-hexagonal-architecture-backend.md) - Architecture hexagonale

---

## Prochaines étapes

1. ✅ Implémentation complète
2. ✅ Tests fonctionnels
3. ⏳ Benchmarks de performance
4. ⏳ Tests de charge (k6, locust)
5. ⏳ Monitoring des performances (Prometheus)
6. ⏳ Optimisation connection pool

---

## Risques et Mitigations

### Risque 1: Complexité async/await

**Impact**: Moyen
**Probabilité**: Moyenne
**Mitigation**:
- Documentation complète
- Exemples de code
- Revue de code stricte

### Risque 2: Bugs concurrence

**Impact**: Élevé
**Probabilité**: Faible
**Mitigation**:
- Tests de charge systématiques
- Monitoring en production
- Rollback possible (psycopg2 conservé)

### Risque 3: Performance non-optimale

**Impact**: Moyen
**Probabilité**: Faible
**Mitigation**:
- Benchmarks avant/après
- Profiling avec py-spy
- Tuning connection pool

---

## Notes

Cette décision a été prise en synergie avec ADR-001 (architecture hexagonale). L'async est maintenant un standard dans l'écosystème Python web, et cette migration positionne le projet pour une scalabilité future.

**Cette décision est considérée comme définitive pour l'architecture actuelle.**
