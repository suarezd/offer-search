# Documentation Offer Search

Bienvenue dans la documentation du projet **Offer Search**, une extension navigateur pour centraliser et gérer les offres d'emploi (LinkedIn, Indeed).

---

## 📚 Table des Matières

### 🏛️ Architecture

1. **[Architecture & ADRs - Vue d'ensemble](adr/ADR.md)** ⭐ - Guide complet de l'architecture hexagonale
   - Architecture hexagonale (Ports & Adapters)
   - Structure du projet (Backend + Frontend)
   - Migration et implémentation
   - Historique et décisions

2. **[Architecture Decision Records (ADR) - Détails](adr/)** - Décisions architecturales spécifiques
   - [ADR-001: Architecture hexagonale backend](adr/001-hexagonal-architecture-backend.md)
   - [ADR-002: Architecture hexagonale frontend](adr/002-hexagonal-architecture-frontend.md)
   - [ADR-003: Opérations asynchrones avec asyncpg](adr/003-async-database-operations.md)
   - [ADR-004: CQRS simple pour le frontend](adr/004-cqrs-simple-frontend.md)
   - [ADR-005: CQRS simple pour le backend](adr/005-cqrs-simple-backend.md)
   - [ADR-006: Intégration du scraper Indeed](adr/006-integration-indeed-scraper.md)

### 🚀 Démarrage Rapide

- [Installation](#installation)
- [Configuration](#configuration)
- [Développement](#développement)

### 📖 Guides

- [Guide Backend](guides/backend.md) (à venir)
- [Guide Frontend](guides/frontend.md) (à venir)
- [Guide Tests](guides/testing.md) (à venir)

---

## 🎯 Vue d'ensemble du Projet

**Offer Search** est une solution complète pour centraliser les offres d'emploi :

- 🔵 **Extension navigateur** (Chrome & Firefox) pour scraper LinkedIn et Indeed
- 🟢 **API Backend** FastAPI avec PostgreSQL
- 📊 **Interface web** pour visualiser et filtrer les offres

### Stack Technique

#### Frontend
- **TypeScript** - Langage
- **React** - UI framework (extension)
- **Vite** - Build tool
- **Architecture Hexagonale** - Pattern architectural

#### Backend
- **Python 3.11** - Runtime
- **FastAPI** - Web framework
- **SQLAlchemy 2.0** - ORM (async)
- **PostgreSQL 16** - Base de données
- **asyncpg** - Driver async PostgreSQL
- **Architecture Hexagonale** - Pattern architectural

#### Infrastructure
- **Docker & Docker Compose** - Conteneurisation
- **Alembic** - Migrations BDD
- **Uvicorn** - Serveur ASGI

---

## 🏗️ Architecture Globale

```
┌─────────────────────────────────────────────────────────┐
│                 EXTENSION NAVIGATEUR                    │
│  ┌────────────────────────────────────────────────┐    │
│  │  Frontend (TypeScript - Hexa Architecture)     │    │
│  │  ├── domain/    (Entities, Ports)              │    │
│  │  ├── application/ (Services)                   │    │
│  │  └── adapters/  (API, Storage)                 │    │
│  └────────────────────────────────────────────────┘    │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI)                      │
│  ┌────────────────────────────────────────────────┐    │
│  │  Backend (Python - Hexa Architecture)          │    │
│  │  ├── domain/       (Job, IJobRepository)       │    │
│  │  ├── application/  (Use Cases, DTOs)           │    │
│  │  ├── adapters/     (HTTP, PostgreSQL)          │    │
│  │  └── infrastructure/ (DI, Config)              │    │
│  └────────────────────────────────────────────────┘    │
└────────────────┬────────────────────────────────────────┘
                 │ asyncpg
                 ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL 16 Database                     │
│  ┌────────────────────────────────────────────────┐    │
│  │  Tables: jobs, (futures tables...)             │    │
│  │  Indexes: title, company, location, source     │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Installation

### Prérequis

- **Node.js** >= 18
- **Python** 3.11
- **Docker** & Docker Compose
- **Git**

### Clone du projet

```bash
git clone <repository-url>
cd offer-search
```

### Backend

```bash
cd backend

# Avec Docker (recommandé)
docker compose up -d

# Ou en local
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API disponible sur: http://localhost:8000

### Frontend (Extension)

```bash
cd extension

# Installation
npm install

# Développement
npm run dev

# Build production
npm run build
```

---

## ⚙️ Configuration

### Backend (.env)

```env
DATABASE_URL=postgresql://offeruser:offerpass@db:5432/offerdb
```

### Frontend

Configuration dans `manifest.json` :
- Permissions navigateur
- API endpoint

---

## 🧪 Tests

### Backend

```bash
cd backend

# Tests unitaires (à venir)
pytest tests/unit/

# Tests d'intégration (à venir)
pytest tests/integration/

# Tests fonctionnels manuels
curl http://localhost:8000/api/jobs/stats
```

### Frontend

```bash
cd extension

# Tests unitaires (à venir)
npm test

# Tests E2E (à venir)
npm run test:e2e
```

---

## 📊 API Endpoints

### Jobs

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/jobs/submit` | POST | Soumettre des jobs |
| `/api/jobs/search` | POST | Rechercher des jobs |
| `/api/jobs/stats` | GET | Statistiques |

### Health

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Health check |

Documentation interactive: http://localhost:8000/docs

---

## 🎓 Ressources d'Apprentissage

### Architecture

- **[Architecture & ADRs - Guide complet](adr/ADR.md)** ⭐ - Vue d'ensemble complète
- [Architecture Decision Records (ADR)](adr/) - Décisions spécifiques détaillées

### Concepts

- **Ports & Adapters**: Le domaine définit des interfaces (ports), les adapters les implémentent
- **Dependency Inversion**: Les dépendances pointent toujours vers le domaine
- **Use Cases**: Chaque opération métier est isolée dans un use case
- **DTOs**: Séparent les modèles API des entités domaine

### Références Externes

- [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/ddd/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

## 🤝 Contribution

### Workflow

1. **Fork** le projet
2. Créer une **branche feature** (`git checkout -b feature/amazing-feature`)
3. **Commit** les changements (`git commit -m 'Add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une **Pull Request**

### Standards de Code

#### Backend (Python)

- **PEP 8** compliance
- **Type hints** partout
- **Docstrings** pour fonctions publiques
- **Tests** pour nouvelle feature

#### Frontend (TypeScript)

- **ESLint** + **Prettier**
- **Types stricts** (no `any`)
- **Tests** pour composants

### Documentation

- Créer un **ADR** pour toute décision architecturale majeure
- Mettre à jour les **guides** si changement d'API
- Commenter le **code complexe**

---

## 🚀 Roadmap

### Court Terme (Sprint 1-2)

- [ ] Tests unitaires backend (domain + application)
- [ ] Tests d'intégration backend (repositories)
- [ ] Tests E2E frontend
- [ ] Documentation API complète
- [ ] Guide de contribution

### Moyen Terme (Sprint 3-6)

- [x] Support Indeed comme source
- [ ] Support Monster comme source
- [ ] Support Welcome to the Jungle
- [ ] Support APEC
- [ ] Cache Redis
- [ ] Pagination cursor-based
- [ ] Authentification JWT
- [ ] Rate limiting

### Long Terme (6+ mois)

- [ ] POC MongoDB (alternative PostgreSQL)
- [ ] API GraphQL
- [ ] Système de notifications
- [ ] Export CSV/PDF
- [ ] Analytics avancées

---

## 📞 Support

- **Issues GitHub**: [Lien]
- **Email**: contact@example.com
- **Documentation**: Ce répertoire

---

## 📄 Licence

[À définir]

---

## 👥 Contributeurs

- **Diego** - Product Owner & Developer
- **Claude (Sonnet 4.5)** - Architecture & Development Assistant

---

## 📝 Historique des Versions

### Version 2.0.0 (2026-01-07)

- ✅ Support Indeed comme deuxième source de scraping
- ✅ Extension multi-sources (LinkedIn + Indeed)
- ✅ Pattern CQRS simple (frontend + backend)
- ✅ Architecture hexagonale backend
- ✅ Support asyncpg
- ✅ Refactoring complet backend
- ✅ Documentation ADR (6 ADRs)

### Version 1.0.0 (2025-12-11)

- ✅ Extension Chrome/Firefox
- ✅ Scraping LinkedIn
- ✅ API Backend FastAPI
- ✅ Base de données PostgreSQL
- ✅ Architecture hexagonale frontend

---

**Dernière mise à jour**: 2026-01-07
