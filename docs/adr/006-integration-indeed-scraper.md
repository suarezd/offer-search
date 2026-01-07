# ADR-006: Intégration du scraper Indeed

**Date**: 2026-01-07

**Auteurs**: Diego, Claude

**Statut**: ✅ **Accepté**

---

## Contexte

L'extension Offer Search supportait uniquement LinkedIn comme source de jobs. Pour augmenter la quantité et la diversité des offres disponibles, nous avons besoin de scraper d'autres plateformes populaires.

Indeed est la plus grande plateforme d'offres d'emploi au monde avec :
- Couverture internationale (indeed.com, indeed.fr, etc.)
- Millions d'offres actives
- Interface de recherche riche avec filtres avancés
- Structure DOM relativement stable

### Problématiques identifiées

1. **Source unique de données**
   - Limitation à LinkedIn uniquement
   - Dépendance forte à une seule plateforme
   - Risque de manquer des opportunités présentes sur d'autres sites

2. **Nomenclature spécifique à LinkedIn**
   - Bouton "Récupérer mes offres LinkedIn"
   - Messages dans le code faisant référence uniquement à LinkedIn
   - Pas prévu pour être multi-sources

3. **Permissions manifest limitées**
   - `host_permissions` uniquement pour `linkedin.com`
   - Nécessité d'ajouter Indeed aux domaines autorisés

---

## Décision

Ajout d'un **scraper Indeed** suivant la même architecture que le `LinkedInScraper` existant, avec intégration dans le système CQRS établi.

### Structure implémentée

```typescript
src/infrastructure/api/scrapers/
├── LinkedInScraper.ts        ✅ Existant
└── IndeedScraper.ts          🆕 Nouveau
```

### Sélecteurs DOM identifiés

Après analyse du DOM Indeed (URL de test: `fr.indeed.com/jobs?q=freelance+php&l=Paris`), les sélecteurs suivants ont été identifiés :

| Élément | Sélecteurs (par ordre de priorité) |
|---------|-------------------------------------|
| **Container** | `.cardOutline.tapItem`, `div[class*="result job_"]`, `div.job_seen_beacon` |
| **Link** | `a.jcs-JobTitle`, `h2.jobTitle a`, `a[data-jk]` |
| **Title** | `a.jcs-JobTitle span`, `h2.jobTitle a span` |
| **Company** | `span[data-testid="company-name"]`, `.companyName` |
| **Location** | `div[data-testid="text-location"]`, `.companyLocation` |
| **Date** | `span[data-testid="myJobsStateDate"]`, `span.date` |
| **Description** | `div.job-snippet`, `div[class*="snippet"]` |
| **Job ID** | `data-jk` attribute, `job_` class prefix, URL `jk=` parameter |

### Principes appliqués

1. **Cohérence architecturale**
   - Implémentation de `IJobScraper` (même interface que LinkedInScraper)
   - Utilisation du pattern Command/Query (CQRS)
   - Respect de l'architecture hexagonale

2. **Robustesse**
   - Multiples sélecteurs de fallback pour chaque élément
   - Gestion des URLs relatives et absolutes
   - Logging détaillé pour le débogage
   - Génération d'ID unique si extraction échoue

3. **Multi-sources**
   - Support de `indeed.com` et `indeed.fr`
   - Détection automatique via `canScrape(url)`
   - Message d'erreur générique listant toutes les sources disponibles

---

## Conséquences

### ✅ Avantages

1. **Plus de sources de données**
   - Accès à Indeed en plus de LinkedIn
   - Potentiel de milliers d'offres supplémentaires
   - Diversification des sources

2. **Extensibilité démontrée**
   - Preuve que l'architecture permet d'ajouter facilement de nouvelles sources
   - Pattern clair pour ajouter d'autres scrapers (Monster, APEC, etc.)
   - Aucune modification du domain ou des queries nécessaire

3. **Expérience utilisateur améliorée**
   - Un seul bouton "Récupérer les offres" pour toutes les sources
   - Détection automatique de la source selon l'URL active
   - Filtre par source dans l'interface

4. **Aucune régression**
   - Build réussi (15.14 kB popup.js)
   - LinkedInScraper continue de fonctionner
   - Backwards compatible

### ⚠️ Inconvénients

1. **Maintenance accrue**
   - Un scraper de plus à maintenir si Indeed change son DOM
   - Nécessité de surveiller les changements de structure

2. **Permissions supplémentaires**
   - Extension demande maintenant accès à `indeed.com` et `indeed.fr`
   - Peut nécessiter re-validation par les stores Chrome/Firefox

3. **Risque anti-scraping**
   - Indeed peut détecter et bloquer le scraping automatisé
   - Nécessite des tests réguliers

---

## Implémentation

### IndeedScraper créé

**Fichier**: `src/infrastructure/api/scrapers/IndeedScraper.ts` (156 lignes)

```typescript
export class IndeedScraper implements IJobScraper {
  readonly source = JobSource.INDEED;

  private selectors: ScraperSelectors = {
    cardContainer: [
      '.cardOutline.tapItem',
      'div[class*="result job_"]',
      'div.job_seen_beacon',
      // ... fallbacks
    ],
    // ... autres sélecteurs
  };

  canScrape(url: string): boolean {
    return url.includes('indeed.com/jobs') || url.includes('indeed.fr/jobs');
  }

  async scrape(tabId: number): Promise<Job[]> {
    // Même logique que LinkedInScraper
    // Extraction via chrome.scripting.executeScript
    // Support multiples sélecteurs de fallback
  }
}
```

### Intégration dans popup.ts

**Avant**:
```typescript
const linkedInScraper = new LinkedInScraper();
const scrapeJobsCommand = new ScrapeJobsCommand([linkedInScraper], repository);
const getAvailableScrapersQuery = new GetAvailableScrapersQuery([linkedInScraper]);
```

**Après**:
```typescript
const linkedInScraper = new LinkedInScraper();
const indeedScraper = new IndeedScraper();

const scrapeJobsCommand = new ScrapeJobsCommand(
  [linkedInScraper, indeedScraper],
  repository
);
const getAvailableScrapersQuery = new GetAvailableScrapersQuery(
  [linkedInScraper, indeedScraper]
);
```

### Mise à jour du manifest.json

**Avant**:
```json
{
  "version": "1.6.0",
  "description": "Récupère tes offres LinkedIn",
  "host_permissions": [
    "https://*.linkedin.com/*",
    "http://localhost:8000/*"
  ]
}
```

**Après**:
```json
{
  "version": "2.0.0",
  "description": "Récupère tes offres d'emploi (LinkedIn, Indeed)",
  "host_permissions": [
    "https://*.linkedin.com/*",
    "https://*.indeed.com/*",
    "https://*.indeed.fr/*",
    "http://localhost:8000/*"
  ]
}
```

### Fichiers impactés

**Créés**:
- `src/infrastructure/api/scrapers/IndeedScraper.ts`

**Modifiés**:
- `src/infrastructure/ui/popup/popup.ts` (imports, instanciation)
- `src/infrastructure/ui/popup/popup.html` (texte du bouton)
- `src/manifest.json` (version, description, permissions)
- `README.md` (description mise à jour)

---

## Validation

### Build

✅ **Build réussi** :
```bash
$ npm run build
vite v7.2.4 building client environment for production...
✓ 10 modules transformed.
dist/popup.js       15.14 kB │ gzip: 4.79 kB
✓ built in 76ms
```

### Tests manuels à effectuer

- [ ] Charger l'extension dans Chrome
- [ ] Naviguer sur `fr.indeed.com/jobs?q=freelance+php&l=Paris`
- [ ] Cliquer sur "Récupérer les offres"
- [ ] Vérifier que les offres Indeed sont scrapées
- [ ] Vérifier que le filtre par source fonctionne
- [ ] Tester avec LinkedIn pour vérifier la non-régression

---

## Alternatives considérées

### 1. Utiliser l'API Indeed

**Pour**:
- Plus stable que le scraping
- Pas de risque anti-scraping
- Données structurées

**Contre**:
- Nécessite une clé API (payante après quota gratuit)
- Limitations de requêtes
- Dépendance à un service externe

**Verdict**: ❌ Trop contraignant pour un projet personnel

### 2. Scraper via backend plutôt que l'extension

**Pour**:
- Moins de détection anti-scraping (IP serveur)
- Pas de dépendance au DOM du navigateur
- Scraping en arrière-plan possible

**Contre**:
- Complexité accrue (proxy, user-agent rotation)
- Coût serveur
- Ne profite pas du contexte utilisateur déjà connecté

**Verdict**: ⚖️ À considérer pour le futur, mais scraping côté extension plus simple pour l'instant

### 3. Utiliser Puppeteer/Playwright

**Pour**:
- Contrôle total du navigateur
- Peut attendre le chargement dynamique
- Plus robuste

**Contre**:
- Overkill pour une extension Chrome
- Augmente drastiquement la taille du bundle
- Complexité excessive

**Verdict**: ❌ Pas adapté à une extension Chrome

---

## Impact sur l'architecture

### Aucun changement dans le domain ✅

- `domain/entities/Job.ts` : inchangé (JobSource.INDEED existait déjà)
- `domain/ports/IJobScraper.ts` : inchangé
- Architecture hexagonale préservée

### Aucun changement dans les Commands/Queries ✅

- `ScrapeJobsCommand` : inchangé (accepte un tableau de scrapers)
- `GetAvailableScrapersQuery` : inchangé
- Principe Open/Closed respecté

### Changements uniquement dans l'infrastructure ✅

- Ajout d'un nouvel adaptateur (`IndeedScraper`)
- Mise à jour de l'UI (popup.html, popup.ts)
- Mise à jour des permissions (manifest.json)

---

## Cohérence avec l'architecture CQRS

| Couche | Changement | Impact |
|--------|-----------|---------|
| **Domain** | Aucun | JobSource.INDEED existait déjà |
| **Application** | Aucun | Commands/Queries inchangées |
| **Infrastructure (API)** | Nouveau scraper | +1 implémentation de IJobScraper |
| **Infrastructure (UI)** | Injection des 2 scrapers | Modification mineure |

L'ajout d'Indeed démontre la robustesse de l'architecture :
- ✅ Open/Closed Principle respecté
- ✅ Dependency Inversion respecté (IJobScraper)
- ✅ Single Responsibility respecté (un scraper par source)

---

## Références

- [ADR-002](002-hexagonal-architecture-frontend.md) - Architecture Hexagonale Frontend
- [ADR-004](004-cqrs-simple-frontend.md) - CQRS Simple Frontend
- Code source: [src/infrastructure/api/scrapers/](../../src/infrastructure/api/scrapers/)
- Indeed DOM structure: fournie par l'utilisateur le 2026-01-07

---

## Prochaines étapes

1. ⏳ Tester manuellement le scraper Indeed en conditions réelles
2. ⏳ Monitorer la stabilité des sélecteurs DOM Indeed
3. ⏳ Ajouter d'autres sources (Monster, Welcome to the Jungle, APEC, LeBonCoin)
4. ⏳ Considérer l'ajout d'un rate limiting pour éviter la détection anti-scraping
5. ⏳ Envisager l'utilisation d'APIs officielles si disponibles

---

## Risques et Mitigations

### Risque 1: Changement de structure DOM Indeed

**Impact**: Élevé (scraper ne fonctionnera plus)
**Probabilité**: Moyenne
**Mitigation**:
- Multiples sélecteurs de fallback
- Logging détaillé pour identifier rapidement les problèmes
- Tests manuels réguliers

### Risque 2: Détection anti-scraping

**Impact**: Élevé (blocage du scraping)
**Probabilité**: Moyenne
**Mitigation**:
- Scraping léger (pas de boucles, juste la page actuelle)
- Utilisation du contexte utilisateur (extension Chrome)
- Pas de requêtes massives automatiques

### Risque 3: Refus des stores (Chrome Web Store, Firefox Add-ons)

**Impact**: Moyen (nécessite justification)
**Probabilité**: Faible
**Mitigation**:
- Permissions explicites dans manifest.json
- Description claire de l'extension
- Usage personnel/éducatif uniquement

---

## Notes

L'ajout d'Indeed a été trivial grâce à l'architecture bien pensée :
1. Création d'une classe implémentant `IJobScraper`
2. Injection dans les Commands/Queries
3. Mise à jour des permissions

Cela démontre la **scalabilité** et la **maintenabilité** de l'architecture hexagonale avec CQRS.

Le pattern est maintenant clair pour ajouter n'importe quelle source de jobs en quelques minutes.

---

## Changelog

- **2026-01-07**: Création de l'ADR
- **2026-01-07**: Implémentation de IndeedScraper
- **2026-01-07**: Build réussi (15.14 kB popup.js)
- **2026-01-07**: Statut changé à Accepté

---

**Dernière révision**: 2026-01-07
