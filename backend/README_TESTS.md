# Tests Backend - Guide d'exécution

Ce guide explique comment exécuter les tests du backend de l'application Offer Search.

## Prérequis

1. **Base de données PostgreSQL** en cours d'exécution
2. **Dépendances Python** installées (`make backend-install`)

## Structure des tests

```
backend/tests/
├── conftest.py                 # Configuration pytest globale
├── fixtures/                   # Fixtures réutilisables
│   └── job_fixtures.py
├── unit/                       # Tests unitaires
│   └── domain/
│       └── test_job_entity.py
├── integration/                # Tests d'intégration
│   └── test_sqlalchemy_job_repository.py
└── functional/                 # Tests fonctionnels BDD
    ├── features/
    │   └── submit_jobs.feature
    └── step_defs/
        └── test_submit_jobs_steps.py
```

## Commandes Makefile

### Tests unitaires (pas de DB requise)
```bash
make test-unit
```
Exécute uniquement les tests marqués `@pytest.mark.unit`.

### Tests d'intégration (DB requise)
```bash
make backend-dev              # Démarrer DB + API
make test-integration
```
Exécute les tests marqués `@pytest.mark.integration`.

### Tests fonctionnels/BDD (API requise)
```bash
make backend-dev              # Démarrer DB + API
make test-functional
```
Exécute les tests marqués `@pytest.mark.functional`.

### Tous les tests
```bash
make backend-dev              # Démarrer DB + API
make test-all
```

### Tests avec couverture
```bash
make backend-dev
make test-coverage
```
Génère un rapport HTML dans `backend/htmlcov/index.html`.

### Tests pour CI
```bash
make test-ci
```
Génère `coverage.xml` et `junit.xml` pour les outils CI/CD.

## Exécution manuelle avec pytest

### Tests unitaires
```bash
cd backend
pytest -m unit -v
```

### Tests d'intégration
```bash
cd backend
export TEST_DATABASE_URL="postgresql+asyncpg://offeruser:offerpass@localhost:5432/offer_search_test"
pytest -m integration -v
```

### Test spécifique
```bash
cd backend
pytest tests/unit/domain/test_job_entity.py::TestJobEntityValidation::test_id_cannot_exceed_50_characters -v
```

### Tests avec pattern
```bash
cd backend
pytest -k "test_save" -v                    # Tous les tests contenant "save"
pytest tests/unit/ -v                       # Tous les tests unitaires
pytest tests/integration/ -v                # Tous les tests d'intégration
```

### Mode watch (relance automatique)
```bash
cd backend
pip install pytest-watch
pytest-watch -v
```

## Variables d'environnement

Les tests utilisent `.env.test` pour la configuration :

```bash
TEST_DATABASE_URL=postgresql+asyncpg://offeruser:offerpass@localhost:5432/offer_search_test
DATABASE_URL=postgresql://offeruser:offerpass@localhost:5432/offerdb
API_HOST=0.0.0.0
API_PORT=8000
```

## Couverture de code

### Rapport terminal
```bash
pytest --cov=app --cov-report=term-missing
```

### Rapport HTML
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Rapport XML (pour CI)
```bash
pytest --cov=app --cov-report=xml
```

## CI/CD (GitHub Actions)

Le workflow `.github/workflows/tests.yml` exécute automatiquement :

1. Tests unitaires
2. Tests d'intégration
3. Génération rapport de couverture
4. Upload vers Codecov

Déclenché sur :
- Push vers `master`, `develop`, `feat/*`
- Pull requests vers `master`, `develop`

## Statistiques des tests

- **Tests unitaires** : 47 tests (Job entity)
- **Tests d'intégration** : 20 tests (Repository)
- **Tests fonctionnels** : 6 scénarios Gherkin

## Dépannage

### Erreur : "Database does not exist"
```bash
make backend-dev
docker exec -it offer-search-db-1 psql -U offeruser -d offerdb -c "CREATE DATABASE offer_search_test;"
```

### Erreur : "Connection refused"
Vérifier que PostgreSQL est démarré :
```bash
docker ps | grep postgres
```

### Erreur : "Module not found"
Réinstaller les dépendances :
```bash
make backend-install
```

### Nettoyer les artefacts de tests
```bash
rm -rf backend/htmlcov backend/.coverage backend/junit.xml backend/coverage.xml
find backend -type d -name __pycache__ -exec rm -rf {} +
find backend -type d -name .pytest_cache -exec rm -rf {} +
```

## Ressources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
