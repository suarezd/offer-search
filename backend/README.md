# Offer Search - Backend API

Backend FastAPI pour centraliser les offres d'emploi LinkedIn de tous les utilisateurs.

## Technologies

- **FastAPI** : Framework web moderne et rapide
- **PostgreSQL** : Base de données relationnelle
- **SQLAlchemy** : ORM Python
- **Alembic** : Migrations de base de données
- **Docker** : Containerisation

## Installation

### Avec Docker (recommandé)

```bash
# Depuis la racine du projet
make backend-dev

# L'API sera disponible sur http://localhost:8000
# La base de données sur localhost:5432
```

### Installation locale

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env

# Démarrer PostgreSQL (avec Docker)
docker run -d \
  --name offer-search-db \
  -e POSTGRES_USER=offeruser \
  -e POSTGRES_PASSWORD=offerpass \
  -e POSTGRES_DB=offerdb \
  -p 5432:5432 \
  postgres:16-alpine

# Lancer l'API
uvicorn app.main:app --reload
```

## Endpoints API

### Santé

- `GET /health` : Vérifier l'état de l'API
- `GET /` : Message de bienvenue

### Jobs

- `POST /api/jobs/submit` : Soumettre des offres
  ```json
  {
    "jobs": [
      {
        "id": "123456",
        "title": "Développeur Python",
        "company": "TechCorp",
        "location": "Paris, France",
        "url": "https://linkedin.com/jobs/view/123456",
        "posted_date": "2024-01-15",
        "description": "Description...",
        "scraped_at": "2024-01-15T10:30:00Z"
      }
    ]
  }
  ```

- `POST /api/jobs/search` : Rechercher des offres
  ```json
  {
    "search": "Python",
    "location": "Paris",
    "company": "TechCorp",
    "limit": 50,
    "offset": 0
  }
  ```

- `GET /api/jobs/stats` : Statistiques globales
  ```json
  {
    "total_jobs": 1234,
    "total_companies": 456,
    "total_locations": 89
  }
  ```

## Structure (Architecture Hexagonale)

```
backend/
├── app/
│   ├── main.py                                      # Point d'entrée FastAPI
│   ├── domain/                                      # ❤️ Cœur métier
│   │   ├── entities/
│   │   │   └── job.py                              # Entité Job avec validations
│   │   ├── ports/
│   │   │   └── job_repository.py                   # Interface IJobRepository
│   │   ├── exceptions/
│   │   │   └── job_exceptions.py                   # Exceptions métier
│   │   └── services/                               # Services domaine (si nécessaire)
│   ├── application/                                 # 🎯 Use Cases
│   │   ├── dto/
│   │   │   └── job_dto.py                          # Data Transfer Objects
│   │   ├── services/                               # Services applicatifs
│   │   └── use_cases/
│   │       ├── submit_jobs.py                      # Cas d'usage : Soumission
│   │       ├── search_jobs.py                      # Cas d'usage : Recherche
│   │       └── get_stats.py                        # Cas d'usage : Statistiques
│   ├── adapters/                                    # 🔌 Interfaces externes
│   │   ├── primary/                                # Adaptateurs primaires
│   │   │   └── http/
│   │   │       └── routes/
│   │   │           └── job_routes.py               # Routes FastAPI
│   │   └── secondary/                              # Adaptateurs secondaires
│   │       └── persistence/
│   │           ├── database.py                     # Configuration async DB
│   │           ├── models/
│   │           │   └── job_model.py                # Modèle SQLAlchemy
│   │           └── sqlalchemy_job_repository.py    # Implémentation du port
│   └── infrastructure/                              # ⚙️ Configuration
│       └── dependencies.py                         # Dependency Injection FastAPI
├── alembic/                                         # Migrations (à configurer)
├── requirements.txt                                 # Dépendances production
├── pyproject.toml                                   # Configuration moderne Python
├── Dockerfile
├── .env.example
└── README.md
```

**Couches de l'architecture hexagonale :**

1. **Domain** (❤️) : Logique métier pure, indépendante des frameworks
2. **Application** (🎯) : Orchestration des use cases
3. **Adapters** (🔌) : Connexion avec le monde extérieur (HTTP, BDD)
4. **Infrastructure** (⚙️) : Configuration des frameworks (FastAPI, SQLAlchemy)

## Développement

### Commandes utiles

```bash
# Démarrer le backend
make backend-dev

# Arrêter le backend
make backend-stop

# Tester l'API
make api-test

# Voir les logs
docker-compose logs -f api

# Accéder au shell de la base de données
docker-compose exec db psql -U offeruser -d offerdb
```

### Documentation interactive

Une fois l'API démarrée :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Base de données

### Modèle Job

| Champ | Type | Description |
|-------|------|-------------|
| id | String(50) | ID unique de l'offre (LinkedIn) |
| title | String(255) | Titre du poste |
| company | String(255) | Nom de l'entreprise |
| location | String(255) | Localisation |
| url | String(500) | URL de l'offre |
| posted_date | String(100) | Date de publication |
| description | Text | Description complète |
| scraped_at | DateTime | Date de scraping |
| created_at | DateTime | Date de création en DB |
| updated_at | DateTime | Date de mise à jour |

### Index

- `idx_title_company` : (title, company)
- `idx_location_company` : (location, company)

## Variables d'environnement

```bash
DATABASE_URL=postgresql://offeruser:offerpass@localhost:5432/offerdb
API_HOST=0.0.0.0
API_PORT=8000
```

## Déploiement

(À venir - instructions pour déployer sur un serveur de production)
