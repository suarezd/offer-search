# Offer Search Extension - Guide d'installation

Extension de navigateur pour centraliser et gérer vos offres d'emploi depuis LinkedIn et Indeed.

## 📦 Installation

### Chrome

1. Téléchargez le fichier `offer-search-extension-v2.0-production.zip`
2. Dézippez le fichier
3. Ouvrez Chrome et allez sur `chrome://extensions/`
4. Activez le "Mode développeur" (toggle en haut à droite)
5. Cliquez sur "Charger l'extension non empaquetée"
6. Sélectionnez le dossier `dist/` dézippé
7. L'extension est installée ! 🎉

### Firefox

1. Téléchargez le fichier `offer-search-extension-v2.0-production.zip`
2. Dézippez le fichier
3. Ouvrez Firefox et allez sur `about:debugging#/runtime/this-firefox`
4. Cliquez sur "Charger un module complémentaire temporaire"
5. Naviguez vers le dossier `dist/` et sélectionnez `manifest.json`
6. L'extension est installée ! 🎉

**Note :** Sur Firefox, l'extension temporaire sera supprimée à la fermeture du navigateur. Pour une installation permanente, l'extension doit être publiée sur Firefox Add-ons.

## 🚀 Utilisation

1. Naviguez vers une page de recherche d'emploi :
   - LinkedIn : `https://www.linkedin.com/jobs/search/`
   - Indeed : `https://www.indeed.com/jobs`

2. Cliquez sur l'icône de l'extension dans la barre d'outils

3. Cliquez sur "Récupérer les offres" pour extraire les offres visibles

4. Les offres sont automatiquement sauvegardées dans le cloud ☁️

5. Utilisez la recherche pour filtrer vos offres par :
   - Titre du poste
   - Entreprise
   - Localisation

## ✨ Fonctionnalités

- ✅ **Scraping automatique** : Extrait les offres depuis LinkedIn et Indeed
- ✅ **Stockage cloud** : Vos données sont sauvegardées sur un backend sécurisé
- ✅ **Recherche avancée** : Filtrez rapidement vos offres
- ✅ **Statistiques** : Visualisez le nombre d'offres collectées
- ✅ **Multi-sources** : Supporte LinkedIn et Indeed
- ✅ **Architecture hexagonale** : Code maintenable et extensible

## 🔒 Sécurité & Confidentialité

- Les données sont stockées sur un serveur backend hébergé sur Railway (https://offer-search-production.up.railway.app)
- La communication utilise HTTPS pour chiffrer les données en transit
- CORS configuré pour n'accepter que les requêtes depuis l'extension
- Aucune donnée n'est partagée avec des tiers

## 🐛 Problèmes connus

Si l'extension ne fonctionne pas :

1. **Vérifiez que vous êtes sur une page de recherche LinkedIn ou Indeed**
   - L'extension ne fonctionne que sur les pages de résultats de recherche

2. **Vérifiez la connexion au backend**
   - Ouvrez la console développeur (F12)
   - Regardez les erreurs réseau

3. **Rechargez l'extension**
   - Chrome : `chrome://extensions/` → Cliquez sur le bouton "Recharger"
   - Firefox : `about:debugging` → Cliquez sur "Recharger"

## 📊 Backend API

L'extension communique avec un backend FastAPI hébergé sur Railway :
- URL : `https://offer-search-production.up.railway.app`
- Documentation API : `https://offer-search-production.up.railway.app/docs`
- Healthcheck : `https://offer-search-production.up.railway.app/health`

## 🛠️ Développement

Pour modifier l'extension :

```bash
# Cloner le repo
git clone <votre-repo>
cd offer-search

# Installer les dépendances
npm install

# Développement avec hot-reload
make dev

# Build pour production
make build

# Build pour Firefox
make build-firefox
```

## 📝 Version

- **Version actuelle** : 2.0.0
- **Dernière mise à jour** : Janvier 2026
- **Backend API** : v2.0.0

## 🤝 Support

Pour toute question ou problème :
1. Consultez la documentation dans le repo GitHub
2. Ouvrez une issue sur GitHub
3. Contactez le support

## 📜 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

---

**Bon recrutement ! 🎯**
