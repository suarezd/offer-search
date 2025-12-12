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

## Structure

```
backend/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── database.py          # Configuration SQLAlchemy
│   ├── models/
│   │   └── job.py           # Modèle Job
│   ├── schemas/
│   │   └── job.py           # Schémas Pydantic
│   └── routers/
│       └── jobs.py          # Routes API
├── alembic/                 # Migrations (à venir)
├── requirements.txt
├── Dockerfile
└── .env.example
```

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
