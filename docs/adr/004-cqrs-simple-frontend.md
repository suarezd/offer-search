# ADR-004: Adoption du pattern CQRS simple pour le frontend

**Date**: 2026-01-07

**Auteurs**: Diego, Claude

**Statut**: ✅ **Accepté**

---

## Contexte

Le frontend de l'extension utilisait une architecture hexagonale classique avec un service monolithique `JobScraperService` qui mélangeait les responsabilités de commande (modification d'état) et de requête (lecture seule).

### Problématiques identifiées

1. **Violation du SRP** (Single Responsibility Principle)
   - Le service `JobScraperService` gérait à la fois le scraping, la soumission, et les recherches
   - 77 lignes de code avec multiples responsabilités

2. **Difficultés de maintenance**
   - Ajout de nouvelles fonctionnalités = modification du service existant
   - Tests complexes car service trop large

3. **Manque de clarté architecturale**
   - Difficile de distinguer les opérations de lecture vs écriture
   - Couplage fort entre différents cas d'usage

4. **Incohérence terminologique**
   - `infrastructure/secondary/` et `infrastructure/primary/` peu explicites
   - Jargon hexagonal difficile pour nouveaux contributeurs

---

## Décision

Adoption du **pattern CQRS simple** (Command Query Responsibility Segregation) pour séparer clairement les use cases en Commands et Queries.

### Structure implémentée

```
src/
├── domain/
│   ├── entities/Job.ts
│   └── ports/                    # ✅ CONSERVÉ (contrats du domain)
│       ├── IJobRepository.ts
│       └── IJobScraper.ts
├── application/
│   ├── commands/                 # 🆕 CQRS - Modifications d'état
│   │   ├── ScrapeJobsCommand.ts
│   │   └── SubmitJobsCommand.ts
│   └── queries/                  # 🆕 CQRS - Lectures seules
│       ├── SearchJobsQuery.ts
│       ├── GetStatsQuery.ts
│       └── GetAvailableScrapersQuery.ts
└── infrastructure/
    ├── ui/                       # 🆕 Renommé (ex-primary)
    │   └── popup/
    └── api/                      # 🆕 Renommé (ex-secondary)
        ├── ApiJobRepository.ts
        └── scrapers/
            └── LinkedInScraper.ts
```

### Principes appliqués

1. **Séparation Command/Query**
   - Commands modifient l'état (scrape, submit)
   - Queries lisent l'état (search, getStats)

2. **Un fichier = Un use case**
   - Chaque command/query = responsabilité unique
   - Facilite tests et maintenance

3. **Nomenclature explicite**
   - `api/` au lieu de `secondary/` (communication réseau)
   - `ui/` au lieu de `primary/` (interface utilisateur)

4. **Conservation des ports**
   - Le domain définit toujours ses propres contrats
   - Inversion de dépendance préservée

---

## Conséquences

### ✅ Avantages

1. **Clarté architecturale**
   - Séparation claire des responsabilités
   - Intention explicite (Command vs Query)
   - Un fichier = un cas d'usage

2. **Meilleure maintenabilité**
   - Ajout de features = nouveau fichier Command/Query
   - Pas de modification de code existant (Open/Closed Principle)
   - Plus facile à comprendre pour nouveaux développeurs

3. **Testabilité améliorée**
   - Tests unitaires isolés par use case
   - Mocks simplifiés (une seule responsabilité)
   - Coverage plus fin

4. **Scalabilité**
   - Facile d'ajouter de nouvelles sources (Indeed, Monster, etc.)
   - Optimisations ciblées par command/query
   - Prépare CQRS avancé si besoin (event sourcing, read models)

5. **Nomenclature accessible**
   - `ui/` et `api/` compréhensibles sans jargon
   - Onboarding facilité pour nouveaux contributeurs

### ⚠️ Inconvénients

1. **Plus de fichiers**
   - 5 nouveaux fichiers vs 1 service monolithique
   - Peut sembler "over-engineering" pour petit projet

2. **Légère duplication**
   - Initialisation des scrapers dans Command et Query
   - Acceptable car responsabilités différentes

3. **Migration initiale**
   - Adaptation des imports existants
   - Mise à jour de la documentation

---

## Alternatives considérées

### 1. Garder le service monolithique

**Pour**:
- Moins de fichiers
- Plus simple pour petit projet

**Contre**:
- Violation du SRP
- Dette technique croissante
- Difficile à maintenir

**Verdict**: ❌ Non durable

### 2. CQRS avancé avec Event Sourcing

**Pour**:
- Historique complet des modifications
- Replay d'événements possible
- Audit trail

**Contre**:
- Overkill pour extension navigateur
- Complexité excessive
- Overhead de stockage

**Verdict**: ❌ Trop complexe

### 3. Architecture par features

**Pour**:
- Organisation par domaine métier
- Cohésion fonctionnelle

**Contre**:
- Moins adapté à CQRS
- Duplication des adapters
- Moins standard

**Verdict**: ⚖️ Possible mais CQRS plus clair

---

## Implémentation

### Commands créées

1. **ScrapeJobsCommand**
   - Trouve le scraper approprié
   - Scrape la page active
   - Soumet les jobs à l'API
   - 58 lignes, responsabilité unique

2. **SubmitJobsCommand**
   - Soumet des jobs à l'API
   - Gestion des erreurs
   - 18 lignes, ultra focalisé

### Queries créées

1. **SearchJobsQuery**
   - Recherche avec filtres
   - Délégation au repository
   - 18 lignes

2. **GetStatsQuery**
   - Récupère les statistiques
   - 16 lignes

3. **GetAvailableScrapersQuery**
   - Liste les scrapers disponibles
   - Retourne les sources supportées
   - 25 lignes

### Refactoring infrastructure

- `infrastructure/secondary/` → `infrastructure/api/`
- `src/popup/` → `infrastructure/ui/popup/`
- Mise à jour du `vite.config.ts`

### Fichiers supprimés

- `src/application/services/JobScraperService.ts` (77 lignes)
- Remplacé par 5 fichiers Commands/Queries (135 lignes total)

---

## Validation

### Critères d'acceptation

- ✅ Build passe (`npm run build`)
- ✅ Extension fonctionnelle dans Chrome
- ✅ Scraping LinkedIn opérationnel
- ✅ Recherche et filtres fonctionnels
- ✅ Statistiques accessibles

### Tests effectués

✅ Build TypeScript réussi sans erreurs
✅ Build Vite réussi (11.89 kB popup.js)
✅ Structure dist/ correcte (manifest, popup, icons)
✅ Imports résolus correctement

---

## Dépendances

### ADRs liés

- [ADR-002](002-hexagonal-architecture-frontend.md) - Base hexagonale conservée
- [ADR-001](001-hexagonal-architecture-backend.md) - Cohérence backend/frontend

### Impact sur l'infrastructure

**Aucun changement** dans les adapters :
- `ApiJobRepository` inchangé (implémente toujours `IJobRepository`)
- `LinkedInScraper` inchangé (implémente toujours `IJobScraper`)
- Les ports du domain restent identiques

**Changements uniquement** dans la couche application et la nomenclature.

---

## Références

- [Martin Fowler - CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Microsoft - CQRS Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- Code source: [src/application/](../../src/application/)

---

## Prochaines étapes

1. ⏳ Monitorer la facilité d'ajout de nouveaux scrapers (Indeed, Monster)
2. ⏳ Évaluer si des Queries nécessitent optimisation (cache)
3. ⏳ Considérer ajout de tests unitaires pour Commands/Queries

---

## Risques et Mitigations

### Risque 1: Sur-ingénierie pour petit projet

**Impact**: Faible
**Probabilité**: Moyenne
**Mitigation**:
- CQRS simple (pas d'event sourcing)
- Pattern standard facilement compréhensible
- Prépare la croissance du projet

### Risque 2: Duplication du setup des scrapers

**Impact**: Faible
**Probabilité**: Élevée
**Mitigation**:
- Acceptable car responsabilités différentes
- Possibilité future de factory si nécessaire
- Complexité actuelle minimale

---

## Notes

Cette refonte améliore significativement la clarté et la maintenabilité du code sans modifier les adapters infrastructure. Le passage de `secondary/primary` à `api/ui` rend l'architecture plus accessible aux contributeurs.

Le pattern CQRS simple est un excellent compromis entre simplicité et organisation claire des responsabilités.

---

## Changelog

- **2026-01-07**: Création de l'ADR
- **2026-01-07**: Implémentation complète et validation
- **2026-01-07**: Statut changé à Accepté

---

**Dernière révision**: 2026-01-07
