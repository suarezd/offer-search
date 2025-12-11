# Guide de contribution

Merci de vouloir contribuer à Offer Search ! Ce guide vous aidera à configurer votre environnement de développement.

## Quick Start

### Avec Makefile (recommandé)

```bash
# Cloner et installer
git clone <url-du-repo>
cd offer-search
make install

# Builder
make build-chrome    # ou make build-firefox

# Développer
make dev
```

### Avec Docker (pour Windows ou pour éviter les problèmes de versions Node)

```bash
# Build et run
make docker-build
make docker-run

# Ou avec docker-compose
docker-compose up app
```

## Workflow de développement

1. **Fork le projet** sur GitHub
2. **Créer une branche** pour votre feature :
   ```bash
   git checkout -b feature/ma-super-feature
   ```
3. **Développer et tester** :
   ```bash
   make build-chrome
   # Charger l'extension dans Chrome pour tester
   ```
4. **Commit vos changements** :
   ```bash
   git add .
   git commit -m "Add: description de la feature"
   ```
5. **Push et créer une Pull Request** :
   ```bash
   git push origin feature/ma-super-feature
   ```

## Structure du code

```
offer-search/
├── src/
│   ├── background.ts           # Service worker (background script)
│   ├── manifest.json           # Manifest Chrome
│   ├── manifest.firefox.json   # Manifest Firefox
│   └── popup/
│       ├── popup.html          # Interface utilisateur
│       └── popup.ts            # Logique du scraping
├── public/icons/               # Icônes de l'extension
├── Makefile                    # Commandes simplifiées
├── Dockerfile                  # Image Docker
└── docker-compose.yml          # Configuration Docker Compose
```

## Standards de code

### TypeScript
- Utiliser TypeScript strict
- Pas de `any` (sauf justifié)
- Typage explicite des interfaces

### Nommage
- Variables : camelCase
- Constantes : UPPER_SNAKE_CASE
- Fonctions : camelCase
- Classes/Interfaces : PascalCase

### Commits
Suivre le format conventional commits :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

Exemples :
```
feat: add support for job filtering
fix: resolve scraping issue on paginated results
docs: update installation instructions for Windows
```

## Tests

(À venir - les tests ne sont pas encore configurés)

```bash
make test
```

## Build pour production

```bash
# Chrome
make build-chrome

# Firefox
make build-firefox

# Les deux avec Docker
make docker-build
make docker-run
# Puis copier le manifest Firefox
cp src/manifest.firefox.json dist/manifest.json
```

## Compatibilité navigateurs

### Chrome
- Manifest V3
- API chrome.* native

### Firefox
- Manifest V3 (Firefox 109+)
- API browser.* (compatible avec chrome.*)
- Différences dans le background script (scripts vs service_worker)

## Debugging

### Chrome
1. Aller sur `chrome://extensions/`
2. Activer le mode développeur
3. Charger l'extension non empaquetée
4. Cliquer sur "Inspecter les vues" pour ouvrir DevTools
5. Les logs du scraping apparaissent dans la console de la page LinkedIn (F12)

### Firefox
1. Aller sur `about:debugging#/runtime/this-firefox`
2. Charger l'extension temporaire
3. Cliquer sur "Inspecter" pour ouvrir les outils de développement
4. Les logs apparaissent dans la console du navigateur

### Logs utiles
- `[Offer Search] Utilisation du sélecteur: ...` : Quel sélecteur CSS a fonctionné
- `[Offer Search] X cartes d'offres détectées` : Nombre de cartes trouvées
- `[Offer Search] Offre trouvée: ... - ID: ...` : Détail de chaque offre extraite

## Problèmes courants

### L'extension ne charge pas les offres
1. Vérifier que vous êtes sur une page LinkedIn Jobs
2. Ouvrir la console (F12) et chercher les logs `[Offer Search]`
3. Vérifier qu'il y a bien des offres visibles sur la page
4. Scroller pour charger plus d'offres

### Les sélecteurs CSS ne fonctionnent pas
LinkedIn change régulièrement sa structure HTML. Si les sélecteurs ne fonctionnent plus :
1. Inspecter la page LinkedIn (F12)
2. Identifier les nouveaux sélecteurs CSS
3. Mettre à jour `src/popup/popup.ts` dans le tableau `cardSelectors`

### Build échoue
```bash
# Nettoyer et réinstaller
make clean
make install
make build-chrome
```

## Ressources

- [Documentation Chrome Extensions](https://developer.chrome.com/docs/extensions/)
- [Documentation Firefox Extensions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)
- [Manifest V3 Migration](https://developer.chrome.com/docs/extensions/migrating/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## Questions ?

Ouvrir une issue sur GitHub avec le tag `question`.
