# Proposition de refonte du site de l'Aronde Dance Club Couthuin

*Document de travail, 1er novembre 2026.*

## 1. Constat sur le site actuel

Le site [arondedanceclub.com](https://www.arondedanceclub.com/) a été créé en 2021 sur Weebly et peu modifié depuis. Il remplit sa fonction de base, mais il donne une image datée et vide du club.

| Aspect | Aujourd'hui | Conséquence |
|---|---|---|
| Apparence | Thème Weebly par défaut, noir et blanc, logo minuscule (52 px), couleurs du logo jamais utilisées | Le site ne ressemble pas au club |
| Photos | Une seule photo réelle (la salle, assombrie), quatre icônes génériques, galerie de 2022 | Rien ne donne envie de venir danser |
| Page d'accueil | Pas d'horaire, pas de tarif, pas d'adresse | Le visiteur doit chercher l'essentiel |
| Calendrier | Dates de septembre 2026 déjà passées, une entrée sans date, une sans intitulé | Le site semble abandonné |
| Téléphone | Mise en page correcte mais menus et textes peu lisibles | Expérience moyenne sur mobile, qui représente la majorité des visites |
| Technique | jQuery 1.8 (2012), bandeau « Propulsé par Weebly », pas d'image de partage pour Facebook ou WhatsApp | Partages peu attrayants, pas de contrôle sur l'hébergement |

Le contenu existant est en revanche sain et suffisant pour une première version : neuf danses, deux niveaux plus une répétition, tarif, cours d'essai gratuit, biographie du professeur, comité, adresse, formulaire de contact.

## 2. Objectifs

1. Donner une image moderne et chaleureuse, fidèle au logo (hirondelle, marine, rouge).
2. Répondre en un écran aux trois questions du visiteur : quand, où, combien.
3. Mettre en avant le cours d'essai gratuit et faciliter la prise de contact.
4. Être irréprochable sur téléphone.
5. Permettre au comité de mettre à jour calendrier, tarif et photos sans toucher à la mise en page.

## 3. Six pistes visuelles

Six maquettes de la page d'accueil ont été réalisées avec le même contenu : trois mises en page, chacune en deux palettes (V1 à V3 autour du marine du logo, V4 à V6 dans d'autres tons). Le comparatif détaillé et la recommandation se trouvent dans [`design/COMPARATIF.md`](design/COMPARATIF.md).

| | V1 « Salon » | V2 « Soirée » | V3 « Hirondelle » |
|---|---|---|---|
| Ambiance | Élégante et chaleureuse | Sombre et spectaculaire | Lumineuse et conviviale |
| Pour qui | Le public actuel du club | Une image très « moderne » | Attirer de nouveaux couples |
| Recommandation | Choix sûr | À réserver si de belles photos sont disponibles | Alternative si la priorité est le recrutement |

| | V4 « Bordeaux » | V5 « Terracotta » | V6 « Prune » |
|---|---|---|---|
| Mise en page | Celle de V1 | Celle de V3 | Celle de V2 |
| Ambiance | Bal, velours et or | Chaleur méditerranéenne | Soirée feutrée |
| Recommandation | Alternative chaude à V1 | La plus accueillante | Alternative à V2 sans bleu |

Liens de consultation en ligne : voir la section « Liens » en fin de document (liens privés, à partager depuis le menu Partager de chaque page).

## 4. Structure proposée du nouveau site

Les adresses des pages sont conservées (`/cours`, `/professeurs`, `/calendrier`, `/galerie`, `/comite`, `/contact`) pour ne pas casser les liens existants.

- **Accueil** : accroche, informations pratiques, les neuf danses, prochains événements, le professeur, aperçu de la galerie, contact.
- **Cours** : niveaux, horaires, saison, tarif et remboursement mutuelle, salle avec plan d'accès.
- **Professeur** : photo, biographie, titres, liens vers la [Ligue de la Danse asbl](http://www.liguedeladanse.com/) et le club [Tourn'et Danse](https://tournetdanse.be/cours-stages-inscription/) où Etienne Mine enseigne également le perfectionnement.
- **Calendrier** : liste « à venir » et « passés » générée automatiquement à partir d'un simple fichier de dates.
- **Galerie** : grille de photos avec légendes, agrandissement au clic.
- **Le comité** : rôles et noms.
- **Contact** : téléphone, e-mail, formulaire, adresse et plan.
- **Pied de page** : ASBL, affiliation AFCD, emplacements Facebook et Instagram, mentions légales.

## 5. Technique et mise à jour

Le site sera un site statique (générateur Astro) : des pages HTML pré-générées, très rapides, sans base de données ni mises à jour de sécurité à gérer.

Le contenu qui change vit dans quelques petits fichiers texte :

- `evenements.json` : une ligne par date (date, heure, titre, lieu).
- `cours.json` : horaires, saison, cotisation.
- `galerie.json` : liste des photos et légendes.
- `comite.json`, `professeurs.json`, `site.json` (téléphone, e-mail, adresse, liens).

Exemple d'ajout d'un événement :

```json
{ "date": "2027-03-20", "heure": "20h00", "titre": "Soirée dansante de printemps", "lieu": "Hall Héromnisport, Héron" }
```

Un guide pas à pas sera fourni dans le `README.md`. Si le comité préfère un formulaire d'édition en ligne, une interface d'administration légère peut être ajoutée dans un second temps.

## 6. Hébergement et nom de domaine

- Hébergement gratuit possible sur Cloudflare Pages, Netlify ou GitHub Pages (sites statiques).
- Le nom de domaine `arondedanceclub.com` reste la propriété du club ; il suffit de le faire pointer vers le nouvel hébergement le jour de la bascule.
- Formulaire de contact : service gratuit type Formspree ou Netlify Forms (envoi vers l'adresse du club), à configurer à la mise en ligne.
- Prévoir des redirections depuis les anciennes adresses `.html`.

## 7. Contenu à fournir par le club

- Photos récentes des cours et soirées (idéalement horizontales, en bonne résolution), pour remplacer les photos d'illustration.
- Dates de la saison en cours : reprise des cours, portes ouvertes, soirées, fin de saison.
- Un court texte « à propos » ou l'historique du club (année de création, pourquoi « Aronde »).
- Liens Facebook ou Instagram s'ils existent, ou décision d'en créer.
- Texte des mentions légales (numéro d'entreprise de l'ASBL, siège social, responsable de publication).
- Logo en haute résolution (fichier vectoriel si possible).

## 8. Points à confirmer

- Orthographe du nom du professeur : « Mine » sur le site actuel et chez Tourn'et Danse, « Minne » dans certains échanges.
- Le comité liste Jean-Louis Delferriere à la fois comme secrétaire et trésorier.
- La soirée du 11 septembre 2026 à 19h30 annoncée en page d'accueil n'a pas d'intitulé dans le calendrier, qui place les portes ouvertes le 18 septembre.
- Mention du club Tourn'et Danse dans la biographie du professeur : à valider avec lui.
- Affiliation éventuelle à la Ligue de la Danse (le site de la Ligue publie une liste de clubs affiliés).

## 9. Crédits

Photos d'illustration sous licence Pexels, listées dans [`design/variants/assets/placeholders/CREDITS.md`](design/variants/assets/placeholders/CREDITS.md). Les autres images appartiennent au club.

## Liens

**Page d'accès aux six maquettes (lien public, à transmettre au comité) : https://stevemihy.github.io/arondedanceclub/**

Liens individuels sur claude.ai (privés, pour commentaires) :

- V1 « Salon » : https://claude.ai/artifact/8nJ9EP3u2ou2s7WCQRPnVB
- V2 « Soirée » : https://claude.ai/artifact/8UnMc5vrvHWQYMfDCFjBLn
- V3 « Hirondelle » : https://claude.ai/artifact/CgxzKjyiwkSL64bPmSDPWh
- V4 « Bordeaux » : https://claude.ai/artifact/8TbkbVTwNQjyooZyzVt5wD
- V5 « Terracotta » : https://claude.ai/artifact/FfXFMpaJm2HHqDEr3525Cp
- V6 « Prune » : https://claude.ai/artifact/KWyQ543kqZtrnGLdyRYvRx
