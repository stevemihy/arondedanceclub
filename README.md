# Aronde Dance Club Couthuin — refonte du site

Projet de refonte de [arondedanceclub.com](https://www.arondedanceclub.com/).

## État du projet

- **Phase A (en cours)** : six maquettes de page d'accueil à comparer (trois mises en page, deux palettes chacune), voir [`design/COMPARATIF.md`](design/COMPARATIF.md) et [`PROPOSITION.md`](PROPOSITION.md).
- **Phase B (à venir)** : site complet en Astro dans la direction retenue.

## Maquettes

```sh
cd design/variants
python3 build.py          # régénère v1-salon.html … v6-prune.html
open v1-salon.html
```

Le contenu des maquettes est défini une seule fois dans `build.py` (section « contenu ») ; les palettes (`V4_PAL`, `V5_PAL`, `V6_PAL`) sont séparées des mises en page, ce qui permet de combiner n'importe quelle palette avec n'importe quelle structure. Les images sont dans `design/variants/assets/` : `club/` pour les images du club, `placeholders/` pour les photos d'illustration (crédits dans `CREDITS.md`).
