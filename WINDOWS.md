# Installation sur Windows

Ce guide explique comment installer et utiliser Offer Search sur Windows.

## Option 1 : Utiliser Docker (Recommandé)

C'est l'option la plus simple car elle évite les problèmes de versions de Node.js et npm.

### Prérequis
- [Docker Desktop pour Windows](https://www.docker.com/products/docker-desktop/)
- [Git for Windows](https://git-scm.com/download/win) (inclut Git Bash avec make)

### Installation

1. Ouvrir Git Bash (inclus avec Git for Windows)

2. Cloner le repository :
```bash
git clone <url-du-repo>
cd offer-search
```

3. Build et compilation avec Docker :
```bash
# Build l'image Docker
make docker-build

# Build l'extension
make docker-run
```

4. L'extension est maintenant disponible dans le dossier `dist/`

### Builder pour Chrome ou Firefox

```bash
# Pour Chrome
make docker-run

# Pour Firefox (après avoir build)
cp src/manifest.firefox.json dist/manifest.json
```

## Option 2 : Installation locale avec Node.js

### Prérequis
- [Node.js v18+](https://nodejs.org/) (choisir la version LTS)
- [Git for Windows](https://git-scm.com/download/win)

### Installation

1. Ouvrir PowerShell ou Git Bash

2. Cloner le repository :
```bash
git clone <url-du-repo>
cd offer-search
```

3. Avec Git Bash (recommandé - inclut make) :
```bash
make install
make build-chrome
```

4. Avec PowerShell (sans make) :
```powershell
npm install
npm run build

# Pour Firefox
Copy-Item src\manifest.firefox.json dist\manifest.json
```

## Option 3 : Installation avec WSL2 (Windows Subsystem for Linux)

Si vous utilisez WSL2, suivez simplement les instructions Linux du README principal.

```bash
# Dans WSL2 (Ubuntu)
make install
make build-chrome
```

## Charger l'extension

### Chrome
1. Ouvrir Chrome et aller sur `chrome://extensions/`
2. Activer le **Mode développeur** (toggle en haut à droite)
3. Cliquer sur **Charger l'extension non empaquetée**
4. Sélectionner le dossier `dist\`

### Firefox
1. Ouvrir Firefox et aller sur `about:debugging#/runtime/this-firefox`
2. Cliquer sur **Charger un module complémentaire temporaire**
3. Sélectionner le fichier `dist\manifest.json`

## Dépannage

### Make n'est pas reconnu
- Installer Git for Windows (inclut Git Bash avec make)
- Ou utiliser les commandes npm directement dans PowerShell

### Docker ne démarre pas
- Vérifier que Docker Desktop est lancé
- Vérifier que la virtualisation est activée dans le BIOS

### Erreur de permissions avec Docker
- Lancer PowerShell ou Git Bash en tant qu'administrateur
- Redémarrer Docker Desktop

### Node.js : version incorrecte
- Utiliser [nvm-windows](https://github.com/coreybutler/nvm-windows) pour gérer les versions de Node.js
- Ou utiliser Docker pour éviter ces problèmes

## Développement sur Windows

### Avec Docker (recommandé)
```bash
# Ouvrir un shell dans le container
make docker-shell

# Dans le container
npm run build
```

### Avec Node.js local
```bash
# Git Bash
make dev

# PowerShell
npm run dev
```

## Scripts batch alternatifs (pour Windows sans Git Bash)

Créer un fichier `build.bat` :
```batch
@echo off
echo Building Offer Search...
npm run build
echo Build complete!
```

Créer un fichier `build-firefox.bat` :
```batch
@echo off
echo Building Offer Search for Firefox...
npm run build
copy src\manifest.firefox.json dist\manifest.json
echo Firefox build complete!
```

Utilisation :
```cmd
build.bat
build-firefox.bat
```
