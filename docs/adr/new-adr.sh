#!/bin/bash

# Script pour créer un nouvel ADR (Architecture Decision Record)
# Usage: ./new-adr.sh "Titre de la décision"

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier qu'un titre est fourni
if [ -z "$1" ]; then
    echo -e "${RED}❌ Erreur: Vous devez fournir un titre pour l'ADR${NC}"
    echo ""
    echo "Usage: ./new-adr.sh \"Titre de la décision\""
    echo "Exemple: ./new-adr.sh \"Migration vers MongoDB\""
    exit 1
fi

TITLE="$1"

# Trouver le prochain numéro d'ADR
ADR_DIR="$(dirname "$0")"
LAST_ADR=$(ls "$ADR_DIR" | grep -E '^[0-9]{3}-' | sort -r | head -n 1 | cut -d'-' -f1)

if [ -z "$LAST_ADR" ]; then
    NEXT_NUMBER="001"
else
    NEXT_NUMBER=$(printf "%03d" $((10#$LAST_ADR + 1)))
fi

# Créer le nom de fichier (slug du titre)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
FILENAME="${NEXT_NUMBER}-${SLUG}.md"
FILEPATH="${ADR_DIR}/${FILENAME}"

# Obtenir la date actuelle
DATE=$(date +%Y-%m-%d)

# Obtenir le nom de l'utilisateur Git ou utiliser $USER
AUTHOR=$(git config user.name 2>/dev/null || echo "$USER")

# Créer le fichier ADR depuis le template
cat > "$FILEPATH" << EOF
# ADR-${NEXT_NUMBER}: ${TITLE}

**Date**: ${DATE}

**Auteurs**: ${AUTHOR}

**Statut**: 🟡 **Proposé**

---

## Contexte

_Décrivez le contexte dans lequel cette décision est prise._

### Problèmes identifiés

1. **Problème 1**: Description
2. **Problème 2**: Description

### Contraintes

- Contrainte technique
- Contrainte temporelle

---

## Décision

_Décrivez clairement la décision prise._

### Points clés

1. **Point 1**: Explication
2. **Point 2**: Explication

---

## Conséquences

### ✅ Avantages

1. **Avantage 1**
   - Détail

2. **Avantage 2**
   - Détail

### ⚠️ Inconvénients

1. **Inconvénient 1**
   - Impact
   - Mitigation possible

---

## Alternatives considérées

### 1. Alternative 1

**Pour**: Avantages
**Contre**: Inconvénients
**Verdict**: ❌ Raison

### 2. Ne rien faire

**Pour**: Pas de changement
**Contre**: Problème non résolu
**Verdict**: ❌ Raison

---

## Implémentation

### Étapes

1. **Phase 1**: Description
2. **Phase 2**: Description

### Fichiers impactés

- \`path/to/file.py\`

---

## Validation

### Critères d'acceptation

- [ ] Critère 1
- [ ] Critère 2

---

## Références

- [Référence 1](https://example.com)

---

## Notes

_Informations additionnelles._

---

**Dernière révision**: ${DATE}
EOF

echo -e "${GREEN}✅ ADR créé avec succès!${NC}"
echo ""
echo -e "${YELLOW}📄 Fichier:${NC} ${FILEPATH}"
echo -e "${YELLOW}🔢 Numéro:${NC} ADR-${NEXT_NUMBER}"
echo -e "${YELLOW}📝 Titre:${NC} ${TITLE}"
echo -e "${YELLOW}📅 Date:${NC} ${DATE}"
echo ""
echo -e "${GREEN}🎯 Prochaines étapes:${NC}"
echo "  1. Éditer le fichier: ${FILENAME}"
echo "  2. Remplir toutes les sections"
echo "  3. Changer le statut à 'Accepté' une fois validé"
echo "  4. Mettre à jour README.md avec le nouvel ADR"
echo ""

# Ouvrir le fichier dans l'éditeur par défaut (optionnel)
if command -v ${EDITOR:-nano} &> /dev/null; then
    read -p "Voulez-vous ouvrir le fichier maintenant? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} "$FILEPATH"
    fi
fi
