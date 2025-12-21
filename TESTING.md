# Guide de Tests - Offer Search

Ce guide explique comment exécuter tous les types de tests du projet Offer Search sur n'importe quelle plateforme (Linux, macOS, Windows).

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Tests Backend](#tests-backend)
  - [Tests Unitaires](#tests-unitaires)
  - [Tests d'Intégration](#tests-dintégration)
  - [Tests Fonctionnels BDD](#tests-fonctionnels-bdd)
- [Tests E2E avec Selenium](#tests-e2e-avec-selenium)
  - [Architecture Multi-Plateformes](#architecture-multi-plateformes)
  - [Démarrage Rapide](#démarrage-rapide)
  - [Mode Local vs Selenium Grid](#mode-local-vs-selenium-grid)
  - [Tests E2E API](#tests-e2e-api)
  - [Tests E2E Extension](#tests-e2e-extension)
  - [Tests E2E Scraping LinkedIn](#tests-e2e-scraping-linkedin)
- [Couverture de Code](#couverture-de-code)
- [CI/CD](#cicd)
- [Dépannage](#dépannage)

---

## Prérequis

### Pour tous les tests
- **Docker** + **Docker Compose** installés
- **Make** (inclus par défaut sur Linux/macOS, Git Bash sur Windows)

### Pour tests E2E en mode local (optionnel)
- Chrome ou Firefox installé sur votre machine
- Python 3.11+ avec dépendances (`pip install -r backend/requirements.txt`)

**💡 Recommandation** : Utilisez **Selenium Grid via Docker** pour une compatibilité universelle (Linux/macOS/Windows/CI).

---

## Tests Backend

Le backend dispose de 3 types de tests : unitaires, intégration, et fonctionnels (BDD).

### Tests Unitaires

Tests de la logique métier pure (Domain layer) sans dépendances externes.

```bash
# Via Docker (recommandé)
make test-unit

# Localement
cd backend && pytest -m unit -v
```

**Couverture** : 47 tests sur les entités du domaine (`Job`)

### Tests d'Intégration

Tests des adapters (Repository PostgreSQL) avec vraie base de données.

```bash
# 1. Démarrer la base de données
make backend-dev

# 2. Lancer les tests
make test-integration
```

**Couverture** : 20 tests sur `SQLAlchemyJobRepository`

### Tests Fonctionnels BDD

Tests de scénarios métier en Gherkin (pytest-bdd) avec API réelle.

```bash
# 1. Démarrer backend + DB
make backend-dev

# 2. Lancer les tests BDD
make test-functional
```

**Couverture** : 6 scénarios Gherkin (`submit_jobs.feature`)

### Tous les tests backend

```bash
# Démarre automatiquement les services si nécessaire
make test-all
```

---

## Tests E2E avec Selenium

Les tests E2E (End-to-End) vérifient le comportement complet de l'application via un navigateur réel.

### Architecture Multi-Plateformes

Le projet utilise **Selenium Grid** pour garantir la portabilité sur toutes les plateformes :

```
┌─────────────────────────────────────────────────────┐
│              Votre Machine                          │
│  (Linux / macOS / Windows / CI)                     │
│                                                     │
│  ┌─────────────────┐      ┌──────────────────┐    │
│  │  Tests Python   │─────▶│  Selenium Hub    │    │
│  │  (pytest)       │      │  (Docker)        │    │
│  └─────────────────┘      └────────┬─────────┘    │
│                                     │              │
│                          ┌──────────┴──────────┐   │
│                          │                     │   │
│                   ┌──────▼──────┐      ┌──────▼──────┐
│                   │   Chrome    │      │  Firefox    │
│                   │  (Docker)   │      │  (Docker)   │
│                   └─────────────┘      └─────────────┘
└─────────────────────────────────────────────────────┘
```

**Avantages** :
- ✅ Fonctionne sur Linux, macOS, Windows
- ✅ Pas besoin d'installer Chrome/Firefox localement
- ✅ Isolation complète (pas de conflits de versions)
- ✅ Visualisation des tests en temps réel via VNC
- ✅ Même configuration pour développement et CI/CD

### Démarrage Rapide

```bash
# 1. Démarrer tous les services (backend + DB + Selenium Grid)
make start
make selenium-start

# 2. Lancer les tests E2E
make test-e2e-grid

# 3. Visualiser les tests en direct (optionnel)
# Ouvrir dans votre navigateur : http://localhost:7900
# Mot de passe : secret

# 4. Arrêter Selenium Grid
make selenium-stop
```

### Mode Local vs Selenium Grid

#### Mode Grid (Recommandé - Multi-plateformes)

```bash
# Démarrer Selenium Grid avec Chrome
make selenium-start

# Ou avec Firefox
make selenium-start-firefox

# Lancer les tests via Grid
make test-e2e-grid

# Voir les logs
make selenium-logs

# Arrêter Grid
make selenium-stop
```

**Monitoring** :
- Grid UI : http://localhost:4444
- VNC Chrome : http://localhost:7900 (password: `secret`)
- VNC Firefox : http://localhost:7901 (password: `secret`)

#### Mode Local (Développement uniquement)

```bash
# Nécessite Chrome/Firefox installé sur votre machine
make test-e2e-local
```

⚠️ **Limitations du mode local** :
- Nécessite Chrome/Firefox installé
- Différences entre plateformes (versions, drivers)
- Pas de VNC pour visualiser
- Non recommandé pour CI/CD

### Tests E2E API

Teste les endpoints de l'API via un navigateur headless.

```bash
# Via Selenium Grid (recommandé)
make selenium-start
make test-e2e-api

# Ou localement
make test-e2e-api-local
```

**Tests couverts** :
- ✅ Endpoints REST (`/health`, `/api/jobs/*`, `/docs`)
- ✅ CORS headers
- ✅ Gestion d'erreurs (404, 500)

### Tests E2E Extension

Teste le chargement et le comportement de l'extension Chrome.

```bash
# 1. Build l'extension
make build-chrome

# 2. Lancer les tests (mode headed requis)
make test-e2e-extension
```

⚠️ **Note** : Les extensions Chrome ne fonctionnent pas en mode headless, ces tests nécessitent `--headed`.

**Tests couverts** :
- ✅ Chargement de l'extension sans erreur
- ✅ Background script fonctionne
- ✅ Popup accessible

### Tests E2E Scraping LinkedIn

Teste le scraping réel de LinkedIn Jobs.

```bash
# 1. Définir les credentials LinkedIn de test
export LINKEDIN_TEST_EMAIL='votre-email-test@example.com'
export LINKEDIN_TEST_PASSWORD='votre-mot-de-passe-test'

# 2. Lancer les tests
make test-e2e-scraping
```

⚠️ **Important** :
- Nécessite des credentials LinkedIn valides
- **NE JAMAIS** commiter de vrais credentials dans le code
- Utilisez des variables d'environnement ou secrets CI/CD

**Tests couverts** :
- ✅ Page LinkedIn Jobs accessible
- ✅ Job cards présents
- ✅ Sélecteurs CSS valides (titre, entreprise, localisation)
- ✅ Scroll charge plus d'offres

---

## Couverture de Code

### Générer le rapport de couverture

```bash
# 1. Démarrer les services
make backend-dev

# 2. Lancer les tests avec couverture
make test-coverage

# 3. Ouvrir le rapport HTML
# Navigateur : backend/htmlcov/index.html
```

### Rapport terminal

```bash
docker exec offer-search-api-1 python -m pytest --cov=app --cov-report=term-missing
```

### Pour CI/CD

```bash
make test-ci
# Génère : coverage.xml et junit.xml
```

---

## CI/CD

### GitHub Actions (recommandé)

Le projet inclut un workflow CI/CD complet (voir section suivante).

### GitLab CI

```yaml
# .gitlab-ci.yml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - apk add --no-cache make
    - make test-ci
    - make test-e2e-grid
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### Configuration Selenium Grid pour CI

Les tests E2E utilisent automatiquement Selenium Grid en CI via la variable d'environnement `SELENIUM_REMOTE_URL`.

```yaml
# Exemple de configuration CI
env:
  SELENIUM_REMOTE_URL: http://selenium-hub:4444/wd/hub
  BACKEND_URL: http://api:8000
```

---

## Dépannage

### Erreur : "Database does not exist"

```bash
make backend-dev
docker exec -it offer-search-db-1 psql -U offeruser -d offerdb -c "CREATE DATABASE offer_search_test;"
```

### Erreur : "Connection refused" (Selenium Grid)

```bash
# Vérifier que Selenium Grid est démarré
docker ps | grep selenium

# Redémarrer Grid
make selenium-stop
make selenium-start

# Vérifier le status
curl http://localhost:4444/wd/hub/status | jq
```

### Erreur : "ChromeDriver version mismatch"

C'est exactement pourquoi on utilise Selenium Grid ! Mais si vous utilisez le mode local :

```bash
# Mettre à jour webdriver-manager
pip install --upgrade webdriver-manager

# Ou utiliser Grid (recommandé)
make selenium-start
make test-e2e-grid
```

### Extension Chrome ne se charge pas

```bash
# Vérifier que l'extension est buildée
ls -la dist/

# Rebuild si nécessaire
make build-chrome

# Vérifier les logs d'erreur
docker logs selenium-chrome
```

### Tests LinkedIn échouent

Les tests LinkedIn peuvent échouer si :
- Credentials invalides
- LinkedIn a changé sa structure HTML
- Rate limiting de LinkedIn

```bash
# Vérifier les sélecteurs CSS
docker exec offer-search-api-1 python -m pytest tests/e2e/scraping/ -v --headed -m scraping
```

### VNC ne s'affiche pas

```bash
# Vérifier que le port VNC est exposé
docker ps | grep selenium-chrome
# Devrait montrer : 0.0.0.0:7900->7900/tcp

# Accéder à VNC
# Chrome: http://localhost:7900 (password: secret)
# Firefox: http://localhost:7901 (password: secret)
```

### Nettoyer les artefacts de tests

```bash
# Backend
rm -rf backend/htmlcov backend/.coverage backend/junit.xml backend/coverage.xml
find backend -type d -name __pycache__ -exec rm -rf {} +
find backend -type d -name .pytest_cache -exec rm -rf {} +

# Docker
docker compose down -v  # Supprime aussi les volumes
```

---

## Statistiques des Tests

| Type | Nombre | Durée | Couverture |
|------|--------|-------|------------|
| **Unitaires** | 47 | ~2s | Domain 100% |
| **Intégration** | 20 | ~5s | Repository 95% |
| **Fonctionnels BDD** | 6 | ~8s | Use Cases 90% |
| **E2E API** | 6 | ~10s | Endpoints 85% |
| **E2E Extension** | 3 | ~15s | Extension N/A |
| **E2E Scraping** | 6 | ~30s | Scraper N/A |
| **TOTAL** | **88** | **~70s** | **~92%** |

---

## Commandes Make - Référence Rapide

```bash
# Backend
make test-unit              # Tests unitaires uniquement
make test-integration       # Tests d'intégration (DB requise)
make test-functional        # Tests BDD (API requise)
make test-all               # Tous les tests backend
make test-coverage          # Tests + rapport de couverture HTML
make test-ci                # Tests pour CI (XML + JUnit)

# E2E - Selenium Grid (recommandé)
make selenium-start         # Démarrer Selenium Grid + Chrome
make selenium-start-firefox # Démarrer Selenium Grid + Firefox
make selenium-stop          # Arrêter Selenium Grid
make selenium-logs          # Voir les logs Selenium

make test-e2e-grid          # Tous les tests E2E via Grid
make test-e2e-grid-all      # Tous les E2E + démarre Grid auto

# E2E - Local (dev uniquement)
make test-e2e-local         # Tous les E2E en local
make test-e2e-api-local     # Tests API en local
make test-e2e-extension-local   # Tests extension en local
make test-e2e-scraping-local    # Tests scraping en local
```

---

## Ressources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [pytest-selenium](https://pytest-selenium.readthedocs.io/)
- [Selenium Grid](https://www.selenium.dev/documentation/grid/)
- [Docker Compose](https://docs.docker.com/compose/)

---

**Note** : Ce guide couvre tous les types de tests (Backend, E2E, Selenium Grid). Pour la documentation de l'API backend, consultez [backend/README.md](backend/README.md).
