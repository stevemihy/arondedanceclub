# Aronde Dance Club Couthuin — refonte du site

Projet de refonte de [arondedanceclub.com](https://www.arondedanceclub.com/).

## État du projet

- **Phase A (en cours)** : trois maquettes de page d'accueil à comparer, voir [`design/COMPARATIF.md`](design/COMPARATIF.md) et [`PROPOSITION.md`](PROPOSITION.md).
- **Phase B (à venir)** : site complet en Astro dans la direction retenue.

## Maquettes

```sh
cd design/variants
python3 build.py          # régénère v1-salon.html, v2-soiree.html, v3-hirondelle.html
open v1-salon.html
```

Le contenu des trois maquettes est défini une seule fois dans `build.py` (section « contenu »). Les images sont dans `design/variants/assets/` : `club/` pour les images du club, `placeholders/` pour les photos d'illustration (crédits dans `CREDITS.md`).
