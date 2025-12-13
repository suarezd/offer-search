# ADR-002: Adoption de l'architecture hexagonale pour le frontend

**Date**: 2025-12-12 (implémenté antérieurement, documenté aujourd'hui)

**Auteurs**: Diego, Claude

**Statut**: ✅ **Accepté**

---

## Contexte

Le frontend de l'extension navigateur (Chrome & Firefox) nécessitait une architecture robuste pour :
- Gérer la communication avec l'API backend
- Stocker les données localement
- Supporter plusieurs navigateurs (Chrome, Firefox)
- Faciliter les tests et la maintenance

### Problématiques initiales

1. **Multi-plateforme**: Extension devant fonctionner sur Chrome et Firefox
2. **Persistance locale**: Besoin de stocker les offres d'emploi localement
3. **Communication API**: Interaction avec le backend FastAPI
4. **Testabilité**: Nécessité de tester la logique métier sans dépendances navigateur

---

## Décision

Adoption de l'**Architecture Hexagonale** pour le frontend TypeScript avec la structure suivante :

```
src/
├── domain/                    # Cœur métier (indépendant)
│   ├── entities/             # Job, JobFilter
│   ├── ports/                # IJobRepository, IJobService
│   └── services/             # Services métier
├── application/              # Logique application
│   └── services/             # JobApplicationService
└── adapters/
    ├── primary/              # UI (Popup, Options)
    └── secondary/            # Persistence, API
        ├── ApiJobRepository.ts
        └── LocalJobRepository.ts
```

### Principes appliqués

1. **Indépendance du navigateur**: Le domain ne dépend pas de `chrome.*` ou `browser.*`
2. **Interchangeabilité**: Facile de changer de storage (localStorage → IndexedDB)
3. **Testabilité**: Domain testable sans extension installée

---

## Conséquences

### ✅ Avantages

1. **Support multi-navigateurs simplifié**
   - Adapters spécifiques Chrome/Firefox
   - Domain partagé entre navigateurs
   - Isolation des API navigateur

2. **Testabilité**
   - Tests unitaires du domain sans navigateur
   - Mock des repositories facile
   - Tests E2E isolés

3. **Flexibilité du storage**
   - localStorage actuel
   - Migration vers IndexedDB possible
   - Support offline amélioré

4. **Cohérence avec le backend**
   - Même architecture côté serveur
   - Vocabulaire partagé
   - Facilite la communication équipe

### ⚠️ Inconvénients

1. **Complexité pour une extension**
   - Plus de fichiers pour un petit projet
   - Overhead pour débutants

2. **Build size**
   - Légèrement plus gros (~10%)
   - Compensé par tree-shaking

---

## Alternatives considérées

### 1. Architecture MVC classique

**Pour**: Simple, bien connue
**Contre**: Couplage fort, difficulté tests
**Verdict**: ❌ Trop couplée

### 2. Architecture Redux-like

**Pour**: State management robuste
**Contre**: Overkill pour extension simple
**Verdict**: ❌ Trop complexe

### 3. Architecture simple (fichiers plats)

**Pour**: Rapide à développer
**Contre**: Non maintenable, non testable
**Verdict**: ❌ Dette technique

---

## Implémentation

### Adapters créés

1. **ApiJobRepository**: Communication avec backend FastAPI
2. **LocalJobRepository**: Stockage localStorage
3. **ChromeStorageAdapter**: API Chrome.storage
4. **FirefoxStorageAdapter**: API browser.storage

### Domain

- **Job**: Entité représentant une offre d'emploi
- **IJobRepository**: Interface pour la persistence
- **IJobService**: Interface pour les services métier

---

## Validation

✅ Extension Chrome fonctionnelle
✅ Extension Firefox compatible
✅ Scraping LinkedIn opérationnel
✅ Sync API backend réussie

---

## Références

- [ADR-001](001-hexagonal-architecture-backend.md) - Architecture backend (cohérence)
- [Chrome Extension Architecture](https://developer.chrome.com/docs/extensions/mv3/architecture-overview/)
- Code source: [src/](../../src/)

---

## Notes

Cette architecture a été implémentée avant le backend. L'ADR-001 a été créé pour aligner le backend sur cette structure, créant une cohérence globale du projet.
