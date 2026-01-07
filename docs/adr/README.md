# Architecture Decision Records (ADR)

Ce répertoire contient les enregistrements des décisions architecturales (ADR) pour le projet Offer Search.

## Qu'est-ce qu'un ADR ?

Un Architecture Decision Record (ADR) est un document qui capture une décision architecturale importante, accompagnée de son contexte et de ses conséquences.

## Format

Chaque ADR suit le format suivant :

```markdown
# [numéro]. [titre de la décision]

Date: YYYY-MM-DD

## Statut

[Proposé | Accepté | Déprécié | Remplacé par ADR-XXX]

## Contexte

Quel est le contexte de cette décision ? Quel problème essayons-nous de résoudre ?

## Décision

Quelle est la décision prise ?

## Conséquences

Quelles sont les conséquences (positives et négatives) de cette décision ?

## Alternatives considérées

Quelles autres options ont été envisagées ?
```

## Index des ADR

| # | Titre | Date | Statut |
|---|-------|------|--------|
| [001](001-hexagonal-architecture-backend.md) | Adoption de l'architecture hexagonale pour le backend | 2025-12-12 | Accepté |
| [002](002-hexagonal-architecture-frontend.md) | Adoption de l'architecture hexagonale pour le frontend | 2025-12-12 | Accepté |
| [003](003-async-database-operations.md) | Utilisation d'asyncpg pour les opérations asynchrones | 2025-12-12 | Accepté |
| [004](004-cqrs-simple-frontend.md) | Adoption du pattern CQRS simple pour le frontend | 2026-01-07 | Accepté |
| [005](005-cqrs-simple-backend.md) | Adoption du pattern CQRS simple pour le backend | 2026-01-07 | Accepté |
| [006](006-integration-indeed-scraper.md) | Intégration du scraper Indeed | 2026-01-07 | Accepté |

## Liens utiles

- [Architecture Decision Records (ADR) - GitHub](https://adr.github.io/)
- [Documentation du projet](../)
- [Guide d'architecture hexagonale](../backend/HEXAGONAL_ARCHITECTURE.md)
