# Offer Search

Extension Chrome pour scraper et centraliser les offres d'emploi LinkedIn.

## Description

Offer Search est une extension Chrome qui permet de récupérer automatiquement les offres d'emploi recommandées sur LinkedIn et de les partager dans une base de données commune accessible à tous les utilisateurs de l'extension.

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

- Node.js (v18+)
- npm ou yarn
- Google Chrome ou Chromium

### Étapes d'installation

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
npm run build
```

4. Charger l'extension dans Chrome :
   - Ouvrir Chrome et aller sur `chrome://extensions/`
   - Activer le **Mode développeur** (toggle en haut à droite)
   - Cliquer sur **Charger l'extension non empaquetée**
   - Sélectionner le dossier `dist/`

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

### Scripts disponibles

- `npm run dev` : Mode développement avec Vite
- `npm run build` : Compilation pour production
- `npm run preview` : Prévisualisation du build

### Recharger l'extension pendant le développement

Après chaque modification :
1. Lancer `npm run build`
2. Aller sur `chrome://extensions/`
3. Cliquer sur le bouton de rechargement ↻ de l'extension

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
