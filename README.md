# Offer Search

Extension Chrome/Firefox pour scraper et centraliser les offres d'emploi LinkedIn.

## Description

Offer Search est une extension Chrome qui permet de récupérer automatiquement les offres d'emploi recommandées sur LinkedIn.

### Objectif du projet

- **Phase 1 (actuelle)** : Scraping des offres LinkedIn et stockage local
- **Phase 2 (à venir)** : Backend FastAPI + PostgreSQL pour centraliser les offres de tous les utilisateurs
- **Phase 3 (future)** : Fonctionnalités avancées (filtres, alertes, statistiques)

## Fonctionnalités actuelles

- ✅ Scraping des offres d'emploi LinkedIn recommandées
- ✅ Support de plusieurs formats de pages LinkedIn :
  - `linkedin.com/jobs/search/`
  - `linkedin.com/jobs/collections/recommended/`
  - Pages paginées avec paramètre `start=`
- ✅ Extraction des informations :
  - Titre du poste
  - Entreprise
  - Localisation
  - Date de publication
  - Description (aperçu)
  - URL de l'offre
- ✅ Stockage local avec `chrome.storage.local`
- ✅ Interface popup responsive
- ✅ Bouton de rafraîchissement pour recharger les offres en cache
- ✅ Logs détaillés pour le débogage

## Installation

### Prérequis

**Option 1 : Installation locale**
- Node.js (v18+)
- npm
- Google Chrome ou Firefox

**Option 2 : Installation avec Docker (recommandé pour Windows)**
- Docker
- make (inclus dans le container)

### Installation rapide avec Makefile

Le projet inclut un Makefile pour simplifier les commandes sur tous les OS (Linux, macOS, Windows avec WSL ou Git Bash).

```bash
# Cloner le repository
git clone <url-du-repo>
cd offer-search

# Voir toutes les commandes disponibles
make help

# Installation locale
make install
make build-chrome    # Pour Chrome
make build-firefox   # Pour Firefox

# Avec Docker (sans installer Node.js)
make docker-build
make docker-run
```

### Installation manuelle (sans Makefile)

#### Installation locale

1. Cloner le repository :
```bash
git clone <url-du-repo>
cd offer-search
```

2. Installer les dépendances :
```bash
npm install
```

3. Compiler l'extension :
```bash
# Pour Chrome
npm run build

# Pour Firefox
npm run build
cp src/manifest.firefox.json dist/manifest.json
```

#### Installation avec Docker

```bash
# Build l'image Docker
docker build -t offer-search .

# Build l'extension
docker run --rm -v "$(pwd)/dist:/app/dist" offer-search

# Ou avec docker-compose
docker-compose up app
```

### Charger l'extension

#### Dans Chrome :
1. Ouvrir Chrome et aller sur `chrome://extensions/`
2. Activer le **Mode développeur** (toggle en haut à droite)
3. Cliquer sur **Charger l'extension non empaquetée**
4. Sélectionner le dossier `dist/`

#### Dans Firefox :
1. Ouvrir Firefox et aller sur `about:debugging#/runtime/this-firefox`
2. Cliquer sur **Charger un module complémentaire temporaire**
3. Sélectionner le fichier `dist/manifest.json`

## Utilisation

1. Aller sur une page LinkedIn Jobs (par exemple : `https://www.linkedin.com/jobs/collections/recommended/`)
2. Scroller pour charger les offres
3. Cliquer sur l'icône de l'extension dans la barre d'outils Chrome
4. Cliquer sur **"Récupérer mes offres LinkedIn"**
5. Les offres s'affichent dans la popup
6. Utiliser le bouton **"Rafraîchir les offres maintenant"** pour recharger les offres en cache

## Structure du projet

```
offer-search/
├── src/
│   ├── background.ts          # Service worker de l'extension
│   ├── manifest.json          # Configuration de l'extension Chrome
│   └── popup/
│       ├── popup.html         # Interface utilisateur de la popup
│       └── popup.ts           # Logique de scraping et d'affichage
├── public/
│   └── icons/                 # Icônes de l'extension
├── dist/                      # Dossier de build (généré)
├── package.json
├── tsconfig.json
└── vite.config.ts             # Configuration Vite
```

## Technologies utilisées

- **TypeScript** : Langage de développement
- **Vite** : Build tool rapide et moderne
- **Chrome Extension Manifest V3** : Dernière version des extensions Chrome
- **chrome.scripting.executeScript** : Injection de script pour le scraping

## Développement

### Commandes Makefile disponibles

```bash
make help              # Afficher toutes les commandes
make install           # Installer les dépendances
make build             # Build pour Chrome
make build-chrome      # Build pour Chrome (explicite)
make build-firefox     # Build pour Firefox
make dev               # Lancer le serveur de développement
make clean             # Nettoyer les artifacts de build
make docker-build      # Build l'image Docker
make docker-run        # Build l'extension dans Docker
make docker-shell      # Ouvrir un shell dans le container
```

### Scripts npm disponibles

- `npm run dev` : Mode développement avec Vite
- `npm run build` : Compilation pour production
- `npm run preview` : Prévisualisation du build

### Recharger l'extension pendant le développement

Après chaque modification :
1. Lancer `make build-chrome` ou `make build-firefox`
2. Aller sur `chrome://extensions/` ou `about:debugging`
3. Cliquer sur le bouton de rechargement ↻ de l'extension

### Développement avec Docker

```bash
# Ouvrir un shell dans le container pour développer
make docker-shell

# Dans le container
npm run build
npm run dev
```

## Roadmap

### Phase 1 : Extension Chrome ✅
- [x] Scraping des offres LinkedIn
- [x] Stockage local
- [x] Interface popup basique
- [x] Support de plusieurs formats de pages

### Phase 2 : Backend centralisé (en cours)
- [ ] API FastAPI avec Python
- [ ] Base de données PostgreSQL
- [ ] Endpoints pour soumettre et récupérer les offres
- [ ] Déduplication automatique des offres
- [ ] Cache local avec IndexedDB

### Phase 3 : Fonctionnalités avancées
- [ ] Filtres avancés (localisation, type de contrat, technologies)
- [ ] Système d'alertes
- [ ] Statistiques sur les offres
- [ ] Authentification des utilisateurs
- [ ] Export des données (CSV, JSON)

## Notes techniques

### Sélecteurs CSS utilisés

L'extension utilise plusieurs sélecteurs CSS pour s'adapter aux différentes structures de pages LinkedIn :
- `li[data-occludable-job-id]` : Liste principale des offres
- `div.scaffold-layout__list-container li` : Nouvelle structure collections
- `.job-card-container` : Cartes individuelles
- `.jobs-search-results__list-item` : Résultats de recherche

### Permissions Chrome

L'extension nécessite les permissions suivantes (définies dans `manifest.json`) :
- `storage` : Pour stocker les offres localement
- `activeTab` : Pour accéder à l'onglet LinkedIn actif
- `scripting` : Pour injecter le script de scraping
- `https://*.linkedin.com/*` : Pour accéder aux pages LinkedIn

## Contribution

Ce projet est en développement actif. Les contributions sont les bienvenues !

## Licence

À définir
