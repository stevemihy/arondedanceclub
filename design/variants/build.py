#!/usr/bin/env python3
"""Génère les trois maquettes de page d'accueil (V1 Salon, V2 Soirée, V3 Hirondelle).

Le contenu (textes du site actuel, repris tels quels) est défini une seule fois ci-dessous ;
chaque variante ne change que la mise en page et le style.

    python3 build.py            -> écrit v1-salon.html, v2-soiree.html, v3-hirondelle.html (pages complètes)
    python3 build.py --artifact DIR -> écrit en plus les versions sans squelette <html> pour la publication
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).parent

# --------------------------------------------------------------------------- contenu
SITE = {
    "nom": "Aronde Dance Club Couthuin",
    "court": "Aronde Dance Club",
    "asbl": "ASBL Aronde Dance Club Couthuin",
    "tel": "0476.543.223",
    "tel_href": "tel:+32476543223",
    "tel_note": "GSM de la Présidente",
    "email": "adc.couthuin@hotmail.com",
    "salle": "Hall Héromnisport",
    "rue": "Chaussée de Wavre 41",
    "ville": "4217 Héron",
    "maps": "https://www.google.com/maps/search/?api=1&query=H%C3%A9romnisports%2C+Chauss%C3%A9e+de+Wavre+41%2C+4217+H%C3%A9ron",
    "afcd": "https://www.afcd.be",
    "saison": "2026-2027",
    "cotisation": "130 €",
}

NAV = [("Cours", "#cours"), ("Professeur", "#professeur"), ("Calendrier", "#calendrier"),
       ("Galerie", "#galerie"), ("Le comité", "#comite"), ("Contact", "#contact")]

ACCROCHE = "Venez faire vos premiers pas de danse dans une ambiance conviviale et festive !"
GRATUIT = "Le premier cours est gratuit et adapté au niveau de chacun."

DANSES = [  # (nom, famille)
    ("Valse lente", "standard"), ("Valse viennoise", "standard"), ("Tango", "standard"),
    ("Quick step", "standard"), ("Slow fox", "standard"),
    ("Cha-cha", "latine"), ("Rumba", "latine"), ("Samba", "latine"),
    ("Rock", "rock"),
]
FAMILLES = {"standard": "Danses standard", "latine": "Danses latines", "rock": "Rock"}

COURS_INTRO = ("Les cours ont lieu de mi-septembre à mi-avril. Ils sont séparés en deux catégories afin que "
               "chacun puisse apprendre en fonction de son niveau : les cours pour débutants et perfectionnement. "
               "Une répétition optionnelle est également organisée chaque semaine, tous niveaux confondus, "
               "afin de revoir les enchaînements appris lors des cours précédents.")
COURS_ENCADREMENT = "Les entraînements sont encadrés par des danseurs chevronnés et des professeurs."
HORAIRES = [  # (niveau, jour, heure, note)
    ("Débutants", "Vendredi", "19h30", "Premiers pas, aucune expérience requise."),
    ("Perfectionnement", "Vendredi", "20h30", "Pour aller plus loin dans les enchaînements."),
    ("Répétition", "Mercredi", "20h00", "Optionnelle, tous niveaux confondus."),
]
TARIFS = [
    f"La cotisation annuelle pour la saison {SITE['saison']} s'élève à {SITE['cotisation']} par personne et par cours.",
    "Certaines mutuelles remboursent une partie de l'inscription.",
    "Les répétitions sont gratuites à condition d'être en ordre de cotisation.",
]

EVENEMENTS = [  # (jour, mois, titre, détail)
    ("18", "sept. 2026", "Portes ouvertes", "Démonstrations, informations, inscriptions · 19h30 · Hall Héromnisport, Héron"),
    ("11", "sept. 2026", "Soirée d'information", "19h30 · Hall Héromnisport, Héron · intitulé à confirmer"),
    ("—", "sept. 2026", "Reprise des cours", "Hall Héromnisport, Héron · date à confirmer"),
]
EVENEMENTS_NOTE = "Les prochaines dates de la saison seront annoncées ici."

PROF = {
    "nom": "Etienne Mine",
    "avec": "avec Martine De Goÿ",
    "photo": "assets/club/etienne-martine.jpg",
    "paras": [
        "Etienne Mine est « né en dansant » puisque ses parents étaient professeurs de danse. Très jeune, il a suivi "
        "ses premiers cours collectifs et rencontré celle qui deviendra son épouse, Martine De Goÿ.",
        "Pendant 10 ans, à deux, ils ont organisé diverses activités de danse et, après quelques années de compétition "
        "comme amateurs, ils ont suivi la formation professionnelle pour enseigner la danse, ensemble.",
    ],
    "titres": ["Juge national", "Instructeur UBPDM", "Chorégraphe", "Entraîneur sportif",
               "Membre fondateur de Prodanse AKDMi"],
    "liens": [
        ("Ligue de la Danse asbl", "http://www.liguedeladanse.com/"),
        ("Tourn'et Danse (Tournai)", "https://tournetdanse.be/cours-stages-inscription/"),
    ],
}

GALERIE = [
    ("assets/club/galerie/g1.jpg", "Dernier cours de la saison 2021-2022"),
    ("assets/club/galerie/g2.jpg", "Dernier cours de la saison 2021-2022"),
    ("assets/club/galerie/g3.jpg", "Dernier cours de la saison 2021-2022"),
    ("assets/club/galerie/g5.jpg", "Soirée BBQ, 18 juin 2022"),
]

COMITE = [("Présidente", "Ariane Borremans"), ("Secrétaire", "Jean-Louis Delferriere"),
          ("Trésorier", "Jean-Louis Delferriere")]

PLACEHOLDER = "Photo d'illustration"

# --------------------------------------------------------------------------- helpers
def e(s):
    return html.escape(s, quote=True)


def nav_links(cls=""):
    return "".join(f'<li><a class="{cls}" href="{h}">{e(t)}</a></li>' for t, h in NAV)


def danses_par_famille():
    out = {}
    for nom, fam in DANSES:
        out.setdefault(fam, []).append(nom)
    return out


SWALLOW = ('<svg class="swallow" viewBox="0 0 120 80" aria-hidden="true" focusable="false">'
           '<path d="M4 30c14-10 32-12 48-6 10-10 26-18 46-18-10 6-18 14-22 24 8 4 18 12 26 28-10-8-20-13-30-15'
           '-4 8-10 16-20 24 2-8 3-15 2-22-12 4-26 2-50-15z"/></svg>')

ICON_FB = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.3c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.4H7.4V14h2.8v8z"/></svg>')
ICON_IG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM12 3.8c2.7 0 3 0 4 .1 2.7.1 3.9 1.4 4 4 .1 1 .1 1.4.1 4.1s0 3-.1 4.1c-.1 2.6-1.4 3.9-4 4-1 .1-1.4.1-4 .1s-3 0-4-.1c-2.7-.1-3.9-1.4-4-4C3.9 15 3.8 14.7 3.8 12s0-3 .1-4.1c.1-2.6 1.4-3.9 4-4 1-.1 1.4-.1 4.1-.1zM12 2C9.3 2 8.9 2 7.9 2.1 4.2 2.2 2.2 4.2 2.1 7.9 2 8.9 2 9.3 2 12s0 3.1.1 4.1c.2 3.7 2.2 5.7 5.8 5.8 1 .1 1.4.1 4.1.1s3.1 0 4.1-.1c3.7-.2 5.7-2.2 5.8-5.8.1-1 .1-1.4.1-4.1s0-3.1-.1-4.1c-.2-3.7-2.2-5.7-5.8-5.8C15.1 2 14.7 2 12 2z"/></svg>')


def social_slots(label_cls=""):
    """Emplacements réservés : le club n'a pas (encore) de page publique. Rendus en 'bientôt'."""
    return (f'<div class="social"><span class="{label_cls}">Suivez-nous</span>'
            f'<span class="soc" title="Facebook — lien à ajouter">{ICON_FB}</span>'
            f'<span class="soc" title="Instagram — lien à ajouter">{ICON_IG}</span>'
            f'<small>liens à venir</small></div>')


def contact_form(idp):
    return f'''
<form class="form" id="{idp}-form" novalidate>
  <div class="row2">
    <label for="{idp}-prenom">Prénom <span aria-hidden="true">*</span><input id="{idp}-prenom" name="prenom" type="text" autocomplete="given-name" required></label>
    <label for="{idp}-nom">Nom <span aria-hidden="true">*</span><input id="{idp}-nom" name="nom" type="text" autocomplete="family-name" required></label>
  </div>
  <label for="{idp}-email">E-mail <span aria-hidden="true">*</span><input id="{idp}-email" name="email" type="email" autocomplete="email" required></label>
  <label for="{idp}-msg">Message <span aria-hidden="true">*</span><textarea id="{idp}-msg" name="message" rows="5" required></textarea></label>
  <p class="form-note">* Champ obligatoire</p>
  <button class="btn btn-primary" type="submit">Envoyer</button>
  <p class="form-ok" id="{idp}-ok" hidden role="status">Maquette : l'envoi du formulaire sera activé sur le site définitif. En attendant, écrivez-nous à {e(SITE["email"])}.</p>
</form>'''


FORM_JS = '''
<script>
(function(){
  var f=document.querySelector('form.form'); if(!f) return;
  f.addEventListener('submit',function(ev){ev.preventDefault();
    var ok=f.querySelector('.form-ok'); if(!f.checkValidity()){f.reportValidity();return;}
    ok.hidden=false; ok.scrollIntoView({block:'nearest'});});
  var b=document.querySelector('.menu-btn'), n=document.querySelector('.site-nav');
  if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});
    n.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){n.classList.remove('open');b.setAttribute('aria-expanded','false');});});}
})();
</script>'''


def wrap(title, fonts, css, body, artifact=False):
    head = (f'<title>{e(title)}</title>\n'
            f'<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">\n'
            f'<style>\n{css}\n</style>\n')
    if artifact:
        return head + body + FORM_JS
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="Maquette — {e(SITE["nom"])}">\n'
            + head + '</head>\n<body>\n' + body + FORM_JS + '\n</body>\n</html>\n')


# --------------------------------------------------------------------------- blocs communs
def bloc_horaires_rows():
    return "".join(f'<tr><th scope="row">{e(n)}</th><td>{e(j)}</td><td class="num">{e(h)}</td><td class="note">{e(t)}</td></tr>'
                   for n, j, h, t in HORAIRES)


def bloc_evenements(cls_item="ev"):
    items = "".join(
        f'<li class="{cls_item}"><div class="date"><b>{e(j)}</b><span>{e(m)}</span></div>'
        f'<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for j, m, t, d in EVENEMENTS)
    return items


def bloc_prof_titres():
    return "".join(f'<li>{e(t)}</li>' for t in PROF["titres"])


def bloc_prof_liens():
    return " · ".join(f'<a href="{h}" target="_blank" rel="noopener">{e(t)}</a>' for t, h in PROF["liens"])


def bloc_galerie(cls="ph"):
    return "".join(f'<figure class="{cls}"><img src="{s}" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>'
                   for s, c in GALERIE)


def bloc_comite():
    return "".join(f'<li><span class="role">{e(r)}</span><span class="who">{e(n)}</span></li>' for r, n in COMITE)


def bloc_danses_chips(with_family_class=True):
    out = []
    for fam, noms in danses_par_famille().items():
        chips = "".join(f'<li class="chip {fam if with_family_class else ""}">{e(n)}</li>' for n in noms)
        out.append(f'<div class="fam"><h3>{e(FAMILLES[fam])}</h3><ul class="chips">{chips}</ul></div>')
    return "".join(out)


# =========================================================================== V1 — SALON
V1_CSS = r'''
/* Layout : programme de bal — colonne centrée, cadres cintrés, filets doubles, bandeau marine. */
:root{
  --ivoire:#f7f3ea; --papier:#fffdf8; --encre:#1b2440; --encre-2:#3a4260; --mute:#5c6280;
  --rouge:#b4262f; --rouge-fonce:#8f1d25; --or:#c9a96a; --filet:#dcd3c0; --marine:#1b2440; --marine-2:#243055;
  --sur-marine:#f7f3ea; --ombre:0 18px 40px -24px rgba(27,36,64,.45);
  --f-display:"Cormorant Garamond",Georgia,"Times New Roman",serif; --f-body:"Source Sans 3","Source Sans Pro",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --ivoire:#141826; --papier:#1b2032; --encre:#f1ecdf; --encre-2:#d4cfc2; --mute:#a7a89d; --rouge:#e06b72; --rouge-fonce:#c94d55;
  --or:#c9a96a; --filet:#2e3550; --marine:#0e1220; --marine-2:#171c30; --sur-marine:#f1ecdf; --ombre:0 18px 40px -24px rgba(0,0,0,.8); color-scheme:dark } }
:root[data-theme="dark"]{
  --ivoire:#141826; --papier:#1b2032; --encre:#f1ecdf; --encre-2:#d4cfc2; --mute:#a7a89d; --rouge:#e06b72; --rouge-fonce:#c94d55;
  --or:#c9a96a; --filet:#2e3550; --marine:#0e1220; --marine-2:#171c30; --sur-marine:#f1ecdf; --ombre:0 18px 40px -24px rgba(0,0,0,.8); color-scheme:dark }
*{box-sizing:border-box} html{scroll-behavior:smooth} @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--ivoire);color:var(--encre);font-family:var(--f-body);font-size:1.0625rem;line-height:1.6}
img{max-width:100%;display:block}
a{color:var(--rouge)} a:hover{color:var(--rouge-fonce)}
:focus-visible{outline:3px solid var(--or);outline-offset:3px}
h1,h2,h3{font-family:var(--f-display);font-weight:600;line-height:1.1;margin:0;text-wrap:balance;color:var(--encre)}
h2{font-size:clamp(2rem,4vw,2.9rem)} h3{font-size:1.45rem}
p{margin:0}
.wrap{max-width:72rem;margin-inline:auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.eyebrow{font-family:var(--f-body);font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--rouge);font-weight:600}
.rule{display:flex;align-items:center;gap:1rem;color:var(--or);margin:0 0 1.25rem}
.rule::before,.rule::after{content:"";flex:1;border-top:1px solid var(--filet);border-bottom:1px solid var(--filet);height:3px}
.rule .swallow{width:34px;height:auto;fill:var(--or)}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.8rem 1.4rem;border-radius:999px;font-weight:600;text-decoration:none;border:1.5px solid transparent;font-size:1rem;line-height:1;cursor:pointer;font-family:var(--f-body)}
.btn-primary{background:var(--rouge);color:#fff;border-color:var(--rouge)} .btn-primary:hover{background:var(--rouge-fonce);color:#fff}
.btn-ghost{background:transparent;color:var(--encre);border-color:var(--encre)} .btn-ghost:hover{background:var(--encre);color:var(--ivoire)}
.btn-light{background:transparent;color:var(--sur-marine);border-color:var(--sur-marine)} .btn-light:hover{background:var(--sur-marine);color:var(--marine)}
/* header */
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--ivoire)}
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:color-mix(in srgb,var(--ivoire) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--filet)}
.site-header .wrap{display:flex;align-items:center;gap:1rem;min-height:72px}
.brand{display:flex;align-items:center;gap:.75rem;text-decoration:none;color:var(--encre);margin-right:auto}
.brand img{width:44px;height:44px;border-radius:50%} .brand b{font-family:var(--f-display);font-size:1.35rem;font-weight:600;letter-spacing:.01em} .brand small{display:block;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.site-nav ul{list-style:none;margin:0;padding:0;display:flex;gap:1.5rem} .site-nav a{color:var(--encre);text-decoration:none;font-weight:600;font-size:.95rem} .site-nav a:hover{color:var(--rouge)}
.menu-btn{display:none;background:none;border:1.5px solid var(--encre);color:var(--encre);border-radius:8px;padding:.45rem .7rem;font:inherit;cursor:pointer}
@media (max-width:900px){.site-nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--papier);border-bottom:1px solid var(--filet);padding:1rem max(16px,env(safe-area-inset-left,0px)) 1.25rem}
 .site-nav.open{display:block} .site-nav ul{flex-direction:column;gap:.9rem} .menu-btn{display:inline-block} .header-cta{display:none}}
/* hero */
.hero{padding-block:3.5rem 4rem}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:3rem;align-items:center}
.hero h1{font-size:clamp(2.8rem,6vw,4.8rem);font-weight:500}
.hero h1 em{font-style:italic;color:var(--rouge)}
.hero .lead{font-size:1.2rem;color:var(--encre-2);max-width:34em;margin-top:1.25rem}
.hero .lead b{color:var(--encre)}
.hero .ctas{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.75rem}
.arch{position:relative;border-radius:999px 999px 18px 18px;overflow:hidden;aspect-ratio:4/5;max-width:100%;box-shadow:var(--ombre);border:6px solid var(--papier);outline:1px solid var(--filet)}
.arch img{width:100%;height:100%;object-fit:cover}
.tag{position:absolute;left:12px;bottom:12px;background:rgba(27,36,64,.72);color:#fff;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;padding:.3rem .55rem;border-radius:4px}
@media (max-width:900px){.hero .wrap{grid-template-columns:1fr} .arch{max-width:420px;margin-inline:auto}}
/* bandeau pratique */
.pratique{background:var(--marine);color:var(--sur-marine)}
.pratique .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:0;padding-block:0}
.pratique .cell{padding:1.75rem 1.5rem 1.75rem 0;border-right:1px solid rgba(247,243,234,.18);margin-right:1.5rem}
.pratique .cell:last-child{border-right:0;margin-right:0}
.pratique .eyebrow{color:var(--or)} .pratique h3{color:var(--sur-marine);font-size:1.6rem;margin:.25rem 0 .35rem} .pratique p{opacity:.85;font-size:.98rem}
.pratique a{color:var(--sur-marine)}
@media (max-width:900px){.pratique .wrap{grid-template-columns:1fr} .pratique .cell{border-right:0;margin-right:0;border-bottom:1px solid rgba(247,243,234,.18);padding:1.25rem 0} .pratique .cell:last-child{border-bottom:0}}
/* sections */
section{padding-block:4.5rem}
.sec-head{max-width:40em;margin-bottom:2.25rem}
.sec-head p{color:var(--encre-2);margin-top:.75rem;font-size:1.1rem}
.danses{background:var(--papier);border-top:1px solid var(--filet);border-bottom:1px solid var(--filet)}
.danses .grid{display:grid;grid-template-columns:1.1fr 1fr;gap:3rem;align-items:center}
.fam{margin-bottom:1.25rem} .fam h3{font-size:1.1rem;font-family:var(--f-body);text-transform:uppercase;letter-spacing:.12em;color:var(--mute);font-weight:600;margin-bottom:.5rem}
.chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}
.chip{font-family:var(--f-display);font-size:1.35rem;padding:.35rem .9rem;border:1px solid var(--filet);border-radius:999px;background:var(--ivoire)}
.chip.rock{border-color:var(--rouge);color:var(--rouge)}
.danses figure{margin:0;position:relative;border-radius:18px;overflow:hidden;box-shadow:var(--ombre)} .danses img{aspect-ratio:4/3;object-fit:cover;width:100%}
@media (max-width:900px){.danses .grid{grid-template-columns:1fr}}
/* cours */
.cours .cols{display:grid;grid-template-columns:1.2fr .8fr;gap:3rem}
.table{width:100%;border-collapse:collapse;font-size:1rem;margin-top:1.25rem}
.table th,.table td{text-align:left;padding:.9rem .5rem;border-bottom:1px solid var(--filet);vertical-align:top}
.table th{font-family:var(--f-display);font-size:1.3rem;font-weight:600;white-space:nowrap}
.table .num{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap} .table .note{color:var(--mute)}
.tarif{background:var(--papier);border:1px solid var(--filet);border-radius:18px;padding:1.75rem}
.tarif .prix{font-family:var(--f-display);font-size:3.2rem;line-height:1;color:var(--rouge);font-weight:600} .tarif .prix small{font-size:1rem;font-family:var(--f-body);color:var(--mute);font-weight:400;display:block;margin-top:.25rem}
.tarif ul{margin:1rem 0 0;padding-left:1.1rem;color:var(--encre-2)} .tarif li{margin:.35rem 0}
.gratuit{margin-top:1.25rem;padding:1rem 1.25rem;border-left:3px solid var(--or);background:var(--ivoire);font-size:1rem}
.salle{display:flex;gap:1rem;align-items:center;margin-top:1.5rem;padding:1rem;border:1px solid var(--filet);border-radius:14px;background:var(--papier)}
.salle img{width:96px;height:72px;object-fit:cover;border-radius:8px;flex:none} .salle b{display:block} .salle a{font-size:.95rem}
@media (max-width:900px){.cours .cols{grid-template-columns:1fr} .table .note{display:none}}
/* calendrier */
.calendrier{background:var(--papier);border-top:1px solid var(--filet);border-bottom:1px solid var(--filet)}
.events{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}
.ev{display:flex;gap:1rem;align-items:flex-start;padding:1.25rem;border:1px solid var(--filet);border-radius:14px;background:var(--ivoire)}
.ev .date{flex:none;text-align:center;min-width:3.6rem;border-right:1px solid var(--filet);padding-right:1rem;font-variant-numeric:tabular-nums}
.ev .date b{display:block;font-family:var(--f-display);font-size:2rem;line-height:1;color:var(--rouge)} .ev .date span{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.ev h3{font-size:1.25rem} .ev p{color:var(--encre-2);font-size:.95rem;margin-top:.25rem}
.ev-note{margin-top:1.25rem;color:var(--mute);font-style:italic}
@media (max-width:900px){.events{grid-template-columns:1fr}}
/* prof */
.prof .grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:3rem;align-items:start}
.prof .portrait{border-radius:999px 999px 18px 18px;overflow:hidden;border:6px solid var(--papier);outline:1px solid var(--filet);box-shadow:var(--ombre);aspect-ratio:4/5}
.prof .portrait img{width:100%;height:100%;object-fit:cover;object-position:top}
.prof .paras p{margin-top:1rem;color:var(--encre-2)} .prof .paras p:first-child{margin-top:0}
.titres{list-style:none;padding:0;margin:1.5rem 0 0;display:flex;flex-wrap:wrap;gap:.5rem} .titres li{font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--or);color:var(--encre);padding:.35rem .7rem;border-radius:4px}
.liens{margin-top:1.25rem;font-size:.98rem;color:var(--mute)}
@media (max-width:900px){.prof .grid{grid-template-columns:1fr} .prof .portrait{max-width:380px}}
/* galerie */
.galerie{background:var(--marine);color:var(--sur-marine)} .galerie h2,.galerie .sec-head p{color:var(--sur-marine)} .galerie .eyebrow{color:var(--or)}
.photos{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.ph{margin:0} .ph img{aspect-ratio:1;object-fit:cover;width:100%;border-radius:10px} .ph figcaption{font-size:.8rem;opacity:.75;margin-top:.5rem}
.galerie .btn{margin-top:2rem}
@media (max-width:900px){.photos{grid-template-columns:repeat(2,1fr)}}
/* comité + contact */
.bas .grid{display:grid;grid-template-columns:1fr 1.4fr;gap:3rem}
.comite ul{list-style:none;padding:0;margin:1rem 0 0} .comite li{display:flex;justify-content:space-between;gap:1rem;padding:.8rem 0;border-bottom:1px solid var(--filet)} .comite .role{color:var(--mute)} .comite .who{font-weight:600}
.coord{list-style:none;padding:0;margin:1rem 0 1.5rem;display:grid;gap:.6rem} .coord li b{display:inline-block;min-width:6.5rem;color:var(--mute);font-weight:600;font-size:.9rem;letter-spacing:.06em;text-transform:uppercase}
.form{display:grid;gap:1rem;background:var(--papier);border:1px solid var(--filet);border-radius:18px;padding:1.75rem}
.form label{display:grid;gap:.35rem;font-weight:600;font-size:.95rem} .form input,.form textarea{font:inherit;padding:.7rem .8rem;border:1px solid var(--filet);border-radius:8px;background:var(--ivoire);color:var(--encre);width:100%;min-width:0}
.form .row2{display:grid;grid-template-columns:1fr 1fr;gap:1rem} .form-note{font-size:.85rem;color:var(--mute)} .form-ok{padding:.9rem 1rem;border-left:3px solid var(--or);background:var(--ivoire);font-size:.95rem}
@media (max-width:900px){.bas .grid{grid-template-columns:1fr} .form .row2{grid-template-columns:1fr}}
/* footer */
footer{border-top:1px solid var(--filet);padding-block:2.5rem;font-size:.95rem;color:var(--mute)}
footer .wrap{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:2rem;align-items:start}
footer ul{list-style:none;margin:0;padding:0;display:grid;gap:.4rem} footer a{color:var(--encre);text-decoration:none} footer a:hover{color:var(--rouge)}
.afcd{display:flex;align-items:center;gap:.75rem;margin-top:.75rem} .afcd img{width:72px;background:#fff;border-radius:6px;padding:4px}
.social{display:flex;align-items:center;gap:.6rem;margin-top:.75rem} .soc{width:34px;height:34px;border:1px solid var(--filet);border-radius:50%;display:grid;place-items:center;color:var(--mute)} .soc svg{width:18px;height:18px} .social small{font-size:.8rem}
.maquette{margin-top:2rem;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase}
@media (max-width:900px){footer .wrap{grid-template-columns:1fr}}
'''


def render_v1(artifact=False):
    S = SITE
    body = f'''
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="#top"><img src="assets/club/logo-couleurs.png" alt="" width="44" height="44"><span><b>{e(S["court"])}</b><small>Couthuin · ASBL</small></span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="site-nav" id="nav" aria-label="Navigation principale"><ul>{nav_links()}</ul></nav>
    <a class="btn btn-primary header-cta" href="#contact">Premier cours gratuit</a>
  </div>
</header>
<main id="top">
<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">Danses de salon · Couthuin &amp; Héron</p>
      <h1>Venez apprendre <em>à danser</em></h1>
      <p class="lead">{e(ACCROCHE)} <b>{e(GRATUIT)}</b></p>
      <div class="ctas"><a class="btn btn-primary" href="#cours">Info sur les cours</a><a class="btn btn-ghost" href="#calendrier">Les évènements</a></div>
    </div>
    <div class="arch"><img src="assets/placeholders/cours-groupe.jpg" alt="Des couples de danseurs adultes pendant un cours collectif"><span class="tag">{e(PLACEHOLDER)}</span></div>
  </div>
</section>
<div class="pratique"><div class="wrap">
  <div class="cell"><p class="eyebrow">Quand</p><h3>Le vendredi soir</h3><p>Débutants à 19h30, perfectionnement à 20h30. Répétition le mercredi à 20h00.</p></div>
  <div class="cell"><p class="eyebrow">Où</p><h3>{e(S["salle"])}</h3><p>{e(S["rue"])}, {e(S["ville"])} · <a href="{S["maps"]}" target="_blank" rel="noopener">itinéraire</a></p></div>
  <div class="cell"><p class="eyebrow">Combien</p><h3>{e(S["cotisation"])} par personne</h3><p>et par cours, pour la saison {e(S["saison"])}. Le premier cours est gratuit.</p></div>
</div></div>

<section class="danses" id="danses"><div class="wrap grid">
  <div>
    <div class="rule">{SWALLOW}</div>
    <p class="eyebrow">Ce que nous dansons</p>
    <h2>Neuf danses de couple</h2>
    <p class="sec-head" style="margin:.75rem 0 1.5rem">Le club enseigne la valse lente, la valse viennoise, le tango, le cha-cha, la rumba, le quick step, la samba, le slow fox et le rock.</p>
    {bloc_danses_chips()}
  </div>
  <figure><img src="assets/placeholders/couple-soiree.jpg" alt="Un couple danse lors d'une soirée"><span class="tag">{e(PLACEHOLDER)}</span></figure>
</div></section>

<section class="cours" id="cours"><div class="wrap">
  <div class="rule">{SWALLOW}</div>
  <div class="sec-head"><p class="eyebrow">Les cours</p><h2>De mi-septembre à mi-avril</h2><p>{e(COURS_INTRO)}</p></div>
  <div class="cols">
    <div>
      <table class="table"><caption class="eyebrow" style="text-align:left;margin-bottom:.5rem">Horaires</caption>
        <thead><tr><th scope="col">Niveau</th><th scope="col">Jour</th><th scope="col">Heure</th><th scope="col"></th></tr></thead>
        <tbody>{bloc_horaires_rows()}</tbody></table>
      <p style="margin-top:1rem;color:var(--encre-2)">{e(COURS_ENCADREMENT)}</p>
      <div class="salle"><img src="assets/club/salle-cours.jpg" alt="La salle du Hall Héromnisport pendant un cours"><div><b>{e(S["salle"])}</b>{e(S["rue"])}, {e(S["ville"])}<br><a href="{S["maps"]}" target="_blank" rel="noopener">Ouvrir dans Google Maps</a></div></div>
    </div>
    <div>
      <div class="tarif"><p class="eyebrow">Tarif</p><p class="prix">{e(S["cotisation"])}<small>par personne et par cours · saison {e(S["saison"])}</small></p>
        <ul>{"".join(f"<li>{e(t)}</li>" for t in TARIFS[1:])}</ul>
        <p class="gratuit">{e(GRATUIT)}</p></div>
    </div>
  </div>
</div></section>

<section class="calendrier" id="calendrier"><div class="wrap">
  <div class="rule">{SWALLOW}</div>
  <div class="sec-head"><p class="eyebrow">Calendrier</p><h2>Saison {e(S["saison"])}</h2><p>Portes ouvertes, reprise des cours et soirées du club.</p></div>
  <ul class="events">{bloc_evenements()}</ul>
  <p class="ev-note">{e(EVENEMENTS_NOTE)}</p>
</div></section>

<section class="prof" id="professeur"><div class="wrap">
  <div class="rule">{SWALLOW}</div>
  <div class="grid">
    <div class="portrait"><img src="{PROF["photo"]}" alt="Etienne Mine et Martine De Goÿ"></div>
    <div>
      <p class="eyebrow">Professeur</p><h2>{e(PROF["nom"])} <span style="font-style:italic;font-weight:400;color:var(--mute)">{e(PROF["avec"])}</span></h2>
      <div class="paras" style="margin-top:1.25rem">{"".join(f"<p>{e(p)}</p>" for p in PROF["paras"])}</div>
      <ul class="titres">{bloc_prof_titres()}</ul>
      <p class="liens">Également : {bloc_prof_liens()}</p>
    </div>
  </div>
</div></section>

<section class="galerie" id="galerie"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Galerie</p><h2>La vie du club</h2><p>Dernier cours de la saison 2021-2022 et soirée BBQ du 18 juin 2022.</p></div>
  <div class="photos">{bloc_galerie()}</div>
  <a class="btn btn-light" href="#galerie">Voir toutes les photos</a>
</div></section>

<section class="bas" id="comite"><div class="wrap grid">
  <div class="comite"><div class="rule">{SWALLOW}</div><p class="eyebrow">Le comité</p><h2>Qui fait vivre le club</h2>
    <ul>{bloc_comite()}</ul>
    <p style="margin-top:1.5rem;color:var(--mute);font-size:.95rem">{e(S["asbl"])}, membre de l'<a href="{S["afcd"]}" target="_blank" rel="noopener">AFCD</a>.</p>
  </div>
  <div id="contact"><div class="rule">{SWALLOW}</div><p class="eyebrow">Contact</p><h2>Envie d'essayer ?</h2>
    <ul class="coord">
      <li><b>GSM</b> <a href="{S["tel_href"]}">{e(S["tel"])}</a> <span style="color:var(--mute)">({e(S["tel_note"])})</span></li>
      <li><b>E-mail</b> <a href="mailto:{S["email"]}">{e(S["email"])}</a></li>
      <li><b>Adresse</b> {e(S["salle"])}, {e(S["rue"])}, {e(S["ville"])}</li>
    </ul>
    {contact_form("v1")}
  </div>
</div></section>
</main>
<footer><div class="wrap">
  <div><b style="color:var(--encre);font-family:var(--f-display);font-size:1.3rem">{e(S["asbl"])}</b>
    <div class="afcd"><img src="assets/club/afcd.png" alt="AFCD"><span>fait partie de l'<a href="{S["afcd"]}" target="_blank" rel="noopener">AFCD</a></span></div>
    {social_slots()}</div>
  <ul>{nav_links()}</ul>
  <ul><li><a href="#contact">Mentions légales (à rédiger)</a></li><li><a href="{S["maps"]}" target="_blank" rel="noopener">Plan d'accès</a></li><li class="maquette">Maquette V1 « Salon »</li></ul>
</div></footer>'''
    fonts = "family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Source+Sans+3:wght@400;600"
    return wrap("Aronde Dance Club · V1 Salon", fonts, V1_CSS, body, artifact)


# =========================================================================== V2 — SOIRÉE
V2_CSS = r'''
/* Layout : piste de danse de nuit — photo plein cadre, titres très grands, bandeau défilant des danses, cartes sombres. */
:root{
  --nuit:#0d1222; --nuit-2:#141a2e; --carte:#1a2138; --craie:#f4efe4; --craie-2:#cfcabd; --mute:#8f8fa3;
  --rouge:#e04752; --rouge-btn:#c42f3a; --or:#e2bd7c; --ligne:rgba(244,239,228,.12); --voile:linear-gradient(90deg,rgba(13,18,34,.82) 0%,rgba(13,18,34,.45) 45%,rgba(13,18,34,.15) 100%),linear-gradient(180deg,rgba(13,18,34,.15) 0%,rgba(13,18,34,.35) 60%,#0d1222 100%);
  --f-display:"Bodoni Moda","Didot","Playfair Display",Georgia,serif; --f-body:"Manrope",system-ui,sans-serif; color-scheme:dark;
}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]){
  --nuit:#f6f3ee; --nuit-2:#ebe6dd; --carte:#ffffff; --craie:#161a2b; --craie-2:#3d4257; --mute:#6c6f84; --rouge:#b8262f; --rouge-btn:#b8262f; --or:#9a7a3c; --ligne:rgba(22,26,43,.14);
  --voile:linear-gradient(90deg,rgba(246,243,238,.9) 0%,rgba(246,243,238,.7) 45%,rgba(246,243,238,.3) 100%),linear-gradient(180deg,rgba(246,243,238,.2) 0%,rgba(246,243,238,.5) 60%,#f6f3ee 100%); color-scheme:light } }
:root[data-theme="light"]{
  --nuit:#f6f3ee; --nuit-2:#ebe6dd; --carte:#ffffff; --craie:#161a2b; --craie-2:#3d4257; --mute:#6c6f84; --rouge:#b8262f; --rouge-btn:#b8262f; --or:#9a7a3c; --ligne:rgba(22,26,43,.14);
  --voile:linear-gradient(90deg,rgba(246,243,238,.9) 0%,rgba(246,243,238,.7) 45%,rgba(246,243,238,.3) 100%),linear-gradient(180deg,rgba(246,243,238,.2) 0%,rgba(246,243,238,.5) 60%,#f6f3ee 100%); color-scheme:light }
*{box-sizing:border-box} html{scroll-behavior:smooth} @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto} .marquee ul{animation:none!important}}
body{margin:0;background:var(--nuit);color:var(--craie);font-family:var(--f-body);font-size:1.0625rem;line-height:1.6}
img{max-width:100%;display:block} a{color:var(--or)} a:hover{color:var(--craie)}
:focus-visible{outline:3px solid var(--or);outline-offset:3px}
h1,h2,h3{font-family:var(--f-display);font-weight:500;line-height:1.05;margin:0;text-wrap:balance;color:var(--craie)}
h2{font-size:clamp(2.2rem,5vw,3.6rem)} h3{font-size:1.4rem} p{margin:0}
.wrap{max-width:76rem;margin-inline:auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.eyebrow{font-size:.74rem;letter-spacing:.24em;text-transform:uppercase;color:var(--or);font-weight:700}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.9rem 1.5rem;border-radius:4px;font-weight:700;text-decoration:none;border:1.5px solid transparent;font-size:.95rem;letter-spacing:.04em;text-transform:uppercase;line-height:1;cursor:pointer;font-family:var(--f-body)}
.btn-primary{background:var(--rouge-btn);color:#fff} .btn-primary:hover{filter:brightness(1.12);color:#fff}
.btn-ghost{background:transparent;color:var(--craie);border-color:var(--craie)} .btn-ghost:hover{background:var(--craie);color:var(--nuit)}
/* header */
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--nuit)}
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:color-mix(in srgb,var(--nuit) 80%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--ligne)}
.site-header .wrap{display:flex;align-items:center;gap:1.25rem;min-height:74px}
.brand{display:flex;align-items:center;gap:.75rem;text-decoration:none;color:var(--craie);margin-right:auto}
.brand img{width:42px;height:42px} .brand b{font-family:var(--f-display);font-size:1.3rem;font-weight:500;letter-spacing:.02em}
.site-nav ul{list-style:none;margin:0;padding:0;display:flex;gap:1.6rem} .site-nav a{color:var(--craie-2);text-decoration:none;font-weight:600;font-size:.86rem;letter-spacing:.1em;text-transform:uppercase} .site-nav a:hover{color:var(--or)}
.menu-btn{display:none;background:none;border:1.5px solid var(--craie);color:var(--craie);border-radius:4px;padding:.45rem .7rem;font:inherit;cursor:pointer}
@media (max-width:900px){.site-nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--nuit-2);border-bottom:1px solid var(--ligne);padding:1rem max(16px,env(safe-area-inset-left,0px)) 1.25rem}
 .site-nav.open{display:block} .site-nav ul{flex-direction:column;gap:.9rem} .menu-btn{display:inline-block} .header-cta{display:none}}
/* hero */
.hero{position:relative;isolation:isolate;min-height:min(88svh,820px);display:flex;align-items:flex-end;padding-block:7rem 4rem;overflow:hidden}
.hero .bg{position:absolute;inset:0;z-index:-2} .hero .bg img{width:100%;height:100%;object-fit:cover;object-position:84% 42%}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:var(--voile)}
.hero .wrap{width:100%}
.hero h1{font-size:clamp(3.2rem,9vw,7.5rem);letter-spacing:-.01em;max-width:11em}
.hero h1 em{font-style:italic;color:var(--rouge)}
.hero .lead{font-size:clamp(1.05rem,1.6vw,1.3rem);color:var(--craie-2);max-width:36em;margin-top:1.25rem}
.hero .lead b{color:var(--craie)}
.hero .ctas{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:2rem}
.hero .tag{position:absolute;left:auto;bottom:auto;right:max(16px,env(safe-area-inset-right,0px));top:1rem;background:rgba(13,18,34,.6);color:#f4efe4;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;padding:.3rem .55rem;border-radius:3px}
/* marquee */
.marquee{overflow:hidden;border-top:1px solid var(--ligne);border-bottom:1px solid var(--ligne);padding-block:.9rem;background:var(--nuit-2)}
.marquee ul{list-style:none;margin:0;padding:0;display:flex;gap:3rem;width:max-content;animation:defile 40s linear infinite}
.marquee li{font-family:var(--f-display);font-size:1.5rem;font-style:italic;color:var(--craie-2);white-space:nowrap} .marquee li::after{content:"✦";color:var(--rouge);margin-left:3rem;font-style:normal;font-size:1rem;vertical-align:middle}
@keyframes defile{to{transform:translateX(-50%)}}
/* pratique */
.pratique .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;padding-block:3rem}
.cell{background:var(--carte);border:1px solid var(--ligne);padding:1.6rem;border-radius:6px}
.cell h3{font-size:1.9rem;margin:.4rem 0 .4rem} .cell p{color:var(--craie-2);font-size:.98rem}
@media (max-width:900px){.pratique .wrap{grid-template-columns:1fr}}
section{padding-block:5rem}
.sec-head{max-width:42em;margin-bottom:2.5rem} .sec-head p{color:var(--craie-2);margin-top:.9rem;font-size:1.1rem}
/* danses */
.danses .grid{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}
.fam{margin-bottom:1.5rem} .fam h3{font-family:var(--f-body);font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);font-weight:700;margin-bottom:.6rem}
.chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}
.chip{font-family:var(--f-display);font-size:1.6rem;padding:.2rem .9rem;border:1px solid var(--ligne);border-radius:3px} .chip.rock{border-color:var(--rouge);color:var(--rouge)}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:1rem} .duo figure{margin:0;position:relative;overflow:hidden;border-radius:6px} .duo img{aspect-ratio:3/4;object-fit:cover;width:100%} .duo figure:last-child{margin-top:3rem}
.tag{position:absolute;left:10px;bottom:10px;background:rgba(13,18,34,.65);color:#f4efe4;font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;padding:.3rem .5rem;border-radius:3px}
@media (max-width:900px){.danses .grid{grid-template-columns:1fr}}
.hero .tag{left:auto;bottom:auto;right:max(16px,env(safe-area-inset-right,0px));top:1rem}
/* cours */
.cours{background:var(--nuit-2);border-top:1px solid var(--ligne);border-bottom:1px solid var(--ligne)}
.cours .cols{display:grid;grid-template-columns:1.1fr .9fr;gap:3rem;align-items:start}
.table{width:100%;border-collapse:collapse} .table th,.table td{text-align:left;padding:1rem .5rem;border-bottom:1px solid var(--ligne);vertical-align:top}
.table th{font-family:var(--f-display);font-size:1.5rem;font-weight:500;white-space:nowrap} .table .num{font-variant-numeric:tabular-nums;font-weight:700;color:var(--or);white-space:nowrap} .table .note{color:var(--mute);font-size:.95rem}
.tarif{background:var(--carte);border:1px solid var(--ligne);border-radius:6px;padding:2rem;position:relative;overflow:hidden}
.tarif::before{content:"";position:absolute;inset:auto -40% -60% auto;width:70%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(224,71,82,.35),transparent 60%);pointer-events:none}
.tarif .prix{font-family:var(--f-display);font-size:4rem;line-height:1;color:var(--craie)} .tarif .prix small{display:block;font-family:var(--f-body);font-size:.95rem;color:var(--mute);margin-top:.4rem}
.tarif ul{margin:1.25rem 0 0;padding-left:1.1rem;color:var(--craie-2)} .tarif li{margin:.4rem 0}
.gratuit{margin-top:1.25rem;padding:1rem 1.2rem;border:1px dashed var(--or);color:var(--craie);border-radius:4px}
.salle{display:flex;gap:1rem;align-items:center;margin-top:1.5rem;padding:1rem;border:1px solid var(--ligne);border-radius:6px;background:var(--carte)} .salle img{width:110px;height:76px;object-fit:cover;border-radius:4px;flex:none} .salle b{display:block;font-family:var(--f-display);font-size:1.3rem;font-weight:500}
@media (max-width:900px){.cours .cols{grid-template-columns:1fr} .table .note{display:none}}
/* calendrier */
.events{list-style:none;margin:0;padding:0;display:grid;gap:0;border-top:1px solid var(--ligne)}
.ev{display:grid;grid-template-columns:7rem 1fr;gap:1.5rem;padding:1.5rem 0;border-bottom:1px solid var(--ligne);align-items:start}
.ev .date b{display:block;font-family:var(--f-display);font-size:3rem;line-height:.9;color:var(--rouge);font-variant-numeric:tabular-nums} .ev .date span{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.ev h3{font-size:1.7rem} .ev p{color:var(--craie-2);margin-top:.35rem}
.ev-note{margin-top:1.25rem;color:var(--mute);font-style:italic}
@media (max-width:600px){.ev{grid-template-columns:1fr;gap:.5rem}}
/* prof */
.prof{background:var(--nuit-2);border-top:1px solid var(--ligne);border-bottom:1px solid var(--ligne)}
.prof .grid{display:grid;grid-template-columns:.75fr 1.25fr;gap:3rem;align-items:center}
.prof .portrait{border-radius:6px;overflow:hidden;aspect-ratio:4/5;position:relative} .prof .portrait img{width:100%;height:100%;object-fit:cover;object-position:top}
.prof .portrait::after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 0 1px var(--ligne);border-radius:6px}
.prof .paras p{margin-top:1rem;color:var(--craie-2)} .prof .paras p:first-child{margin-top:0}
.titres{list-style:none;padding:0;margin:1.5rem 0 0;display:flex;flex-wrap:wrap;gap:.5rem} .titres li{font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--or);color:var(--or);padding:.4rem .7rem;border-radius:3px}
.liens{margin-top:1.25rem;color:var(--mute)}
@media (max-width:900px){.prof .grid{grid-template-columns:1fr} .prof .portrait{max-width:380px}}
/* galerie */
.photos{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}
.ph{margin:0;position:relative} .ph img{aspect-ratio:1;object-fit:cover;width:100%;border-radius:4px;filter:saturate(.9)} .ph figcaption{font-size:.78rem;color:var(--mute);margin-top:.5rem}
@media (max-width:900px){.photos{grid-template-columns:repeat(2,1fr)}}
/* bas */
.bas{background:var(--nuit-2);border-top:1px solid var(--ligne)} .bas .grid{display:grid;grid-template-columns:1fr 1.4fr;gap:3rem}
.comite ul{list-style:none;padding:0;margin:1.25rem 0 0} .comite li{display:flex;justify-content:space-between;gap:1rem;padding:.9rem 0;border-bottom:1px solid var(--ligne)} .comite .role{color:var(--mute);font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;align-self:center} .comite .who{font-family:var(--f-display);font-size:1.35rem}
.coord{list-style:none;padding:0;margin:1.25rem 0 1.5rem;display:grid;gap:.6rem} .coord b{display:inline-block;min-width:6.5rem;color:var(--mute);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase}
.form{display:grid;gap:1rem;background:var(--carte);border:1px solid var(--ligne);border-radius:6px;padding:1.75rem}
.form label{display:grid;gap:.35rem;font-weight:600;font-size:.9rem;letter-spacing:.04em} .form input,.form textarea{font:inherit;padding:.75rem .85rem;border:1px solid var(--ligne);border-radius:4px;background:var(--nuit);color:var(--craie);width:100%;min-width:0}
.form .row2{display:grid;grid-template-columns:1fr 1fr;gap:1rem} .form-note{font-size:.85rem;color:var(--mute)} .form-ok{padding:.9rem 1rem;border:1px dashed var(--or);border-radius:4px;font-size:.95rem}
@media (max-width:900px){.bas .grid{grid-template-columns:1fr} .form .row2{grid-template-columns:1fr}}
footer{border-top:1px solid var(--ligne);padding-block:2.5rem;font-size:.92rem;color:var(--mute)}
footer .wrap{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:2rem}
footer ul{list-style:none;margin:0;padding:0;display:grid;gap:.45rem} footer a{color:var(--craie-2);text-decoration:none} footer a:hover{color:var(--or)}
.afcd{display:flex;align-items:center;gap:.75rem;margin-top:.75rem} .afcd img{width:72px;background:#fff;border-radius:4px;padding:4px}
.social{display:flex;align-items:center;gap:.6rem;margin-top:.75rem} .soc{width:34px;height:34px;border:1px solid var(--ligne);border-radius:50%;display:grid;place-items:center;color:var(--mute)} .soc svg{width:18px;height:18px} .social small{font-size:.8rem}
.maquette{margin-top:2rem;font-size:.74rem;letter-spacing:.14em;text-transform:uppercase}
@media (max-width:900px){footer .wrap{grid-template-columns:1fr}}
'''


def render_v2(artifact=False):
    S = SITE
    danses_marquee = "".join(f'<li>{e(n)}</li>' for n, _ in DANSES) * 2
    body = f'''
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="#top"><img src="assets/club/logo-blanc.png" alt="" width="42" height="42"><b>{e(S["court"])}</b></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="site-nav" id="nav" aria-label="Navigation principale"><ul>{nav_links()}</ul></nav>
    <a class="btn btn-primary header-cta" href="#contact">1er cours gratuit</a>
  </div>
</header>
<main id="top">
<section class="hero">
  <div class="bg"><img src="assets/placeholders/valse-bleue.jpg" alt="" aria-hidden="true"></div>
  <span class="tag">{e(PLACEHOLDER)}</span>
  <div class="wrap">
    <p class="eyebrow">Danses de salon · Couthuin &amp; Héron · ASBL</p>
    <h1>Venez apprendre <em>à danser</em></h1>
    <p class="lead">{e(ACCROCHE)} <b>{e(GRATUIT)}</b></p>
    <div class="ctas"><a class="btn btn-primary" href="#cours">Info sur les cours</a><a class="btn btn-ghost" href="#calendrier">Les évènements</a></div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><ul>{danses_marquee}</ul></div>
<div class="pratique"><div class="wrap">
  <div class="cell"><p class="eyebrow">Quand</p><h3>Vendredi soir</h3><p>Débutants à 19h30, perfectionnement à 20h30. Répétition le mercredi à 20h00.</p></div>
  <div class="cell"><p class="eyebrow">Où</p><h3>{e(S["salle"])}</h3><p>{e(S["rue"])}, {e(S["ville"])} · <a href="{S["maps"]}" target="_blank" rel="noopener">itinéraire</a></p></div>
  <div class="cell"><p class="eyebrow">Combien</p><h3>{e(S["cotisation"])} / personne</h3><p>et par cours, saison {e(S["saison"])}. Le premier cours est gratuit.</p></div>
</div></div>

<section class="danses" id="danses"><div class="wrap grid">
  <div><p class="eyebrow">Ce que nous dansons</p><h2>Neuf danses de couple</h2>
    <p class="sec-head" style="margin:.9rem 0 1.5rem">Le club enseigne la valse lente, la valse viennoise, le tango, le cha-cha, la rumba, le quick step, la samba, le slow fox et le rock.</p>
    {bloc_danses_chips()}
  </div>
  <div class="duo">
    <figure><img src="assets/placeholders/tango-parquet.jpg" alt="Un couple danse le tango sur un parquet"><span class="tag">{e(PLACEHOLDER)}</span></figure>
    <figure><img src="assets/placeholders/valse-turquoise.jpg" alt="Un couple en tenue de bal danse une valse"><span class="tag">{e(PLACEHOLDER)}</span></figure>
  </div>
</div></section>

<section class="cours" id="cours"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Les cours</p><h2>De mi-septembre à mi-avril</h2><p>{e(COURS_INTRO)}</p></div>
  <div class="cols">
    <div>
      <table class="table"><thead><tr><th scope="col">Niveau</th><th scope="col">Jour</th><th scope="col">Heure</th><th scope="col"></th></tr></thead><tbody>{bloc_horaires_rows()}</tbody></table>
      <p style="margin-top:1rem;color:var(--craie-2)">{e(COURS_ENCADREMENT)}</p>
      <div class="salle"><img src="assets/club/salle-cours.jpg" alt="La salle du Hall Héromnisport pendant un cours"><div><b>{e(S["salle"])}</b>{e(S["rue"])}, {e(S["ville"])}<br><a href="{S["maps"]}" target="_blank" rel="noopener">Ouvrir dans Google Maps</a></div></div>
    </div>
    <div class="tarif"><p class="eyebrow">Tarif</p><p class="prix">{e(S["cotisation"])}<small>par personne et par cours · saison {e(S["saison"])}</small></p>
      <ul>{"".join(f"<li>{e(t)}</li>" for t in TARIFS[1:])}</ul><p class="gratuit">{e(GRATUIT)}</p></div>
  </div>
</div></section>

<section class="calendrier" id="calendrier"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Calendrier</p><h2>Saison {e(S["saison"])}</h2><p>Portes ouvertes, reprise des cours et soirées du club.</p></div>
  <ul class="events">{bloc_evenements()}</ul>
  <p class="ev-note">{e(EVENEMENTS_NOTE)}</p>
</div></section>

<section class="prof" id="professeur"><div class="wrap grid">
  <div class="portrait"><img src="{PROF["photo"]}" alt="Etienne Mine et Martine De Goÿ"></div>
  <div><p class="eyebrow">Professeur</p><h2>{e(PROF["nom"])}</h2><p style="font-family:var(--f-display);font-style:italic;font-size:1.4rem;color:var(--craie-2);margin-top:.25rem">{e(PROF["avec"])}</p>
    <div class="paras" style="margin-top:1.25rem">{"".join(f"<p>{e(p)}</p>" for p in PROF["paras"])}</div>
    <ul class="titres">{bloc_prof_titres()}</ul>
    <p class="liens">Également : {bloc_prof_liens()}</p>
  </div>
</div></section>

<section class="galerie" id="galerie"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Galerie</p><h2>La vie du club</h2><p>Dernier cours de la saison 2021-2022 et soirée BBQ du 18 juin 2022.</p></div>
  <div class="photos">{bloc_galerie()}</div>
  <a class="btn btn-ghost" style="margin-top:2rem" href="#galerie">Voir toutes les photos</a>
</div></section>

<section class="bas" id="comite"><div class="wrap grid">
  <div class="comite"><p class="eyebrow">Le comité</p><h2>Qui fait vivre le club</h2><ul>{bloc_comite()}</ul>
    <p style="margin-top:1.5rem;color:var(--mute);font-size:.95rem">{e(S["asbl"])}, membre de l'<a href="{S["afcd"]}" target="_blank" rel="noopener">AFCD</a>.</p></div>
  <div id="contact"><p class="eyebrow">Contact</p><h2>Envie d'essayer ?</h2>
    <ul class="coord">
      <li><b>GSM</b> <a href="{S["tel_href"]}">{e(S["tel"])}</a> <span style="color:var(--mute)">({e(S["tel_note"])})</span></li>
      <li><b>E-mail</b> <a href="mailto:{S["email"]}">{e(S["email"])}</a></li>
      <li><b>Adresse</b> {e(S["salle"])}, {e(S["rue"])}, {e(S["ville"])}</li>
    </ul>
    {contact_form("v2")}
  </div>
</div></section>
</main>
<footer><div class="wrap">
  <div><b style="color:var(--craie);font-family:var(--f-display);font-size:1.3rem;font-weight:500">{e(S["asbl"])}</b>
    <div class="afcd"><img src="assets/club/afcd.png" alt="AFCD"><span>fait partie de l'<a href="{S["afcd"]}" target="_blank" rel="noopener">AFCD</a></span></div>
    {social_slots()}</div>
  <ul>{nav_links()}</ul>
  <ul><li><a href="#contact">Mentions légales (à rédiger)</a></li><li><a href="{S["maps"]}" target="_blank" rel="noopener">Plan d'accès</a></li><li class="maquette">Maquette V2 « Soirée »</li></ul>
</div></footer>'''
    fonts = "family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;1,6..96,500&family=Manrope:wght@400;600;700"
    return wrap("Aronde Dance Club · V2 Soirée", fonts, V2_CSS, body, artifact)


# =========================================================================== V3 — HIRONDELLE
V3_CSS = r'''
/* Layout : club de quartier, lumineux — hero scindé avec collage, grandes formes arrondies, pastilles colorées par famille, hirondelle en motif. */
:root{
  --blanc:#ffffff; --gris:#f3f4f8; --encre:#1c2541; --encre-2:#454d6b; --mute:#616884; --rouge:#d8323c; --rouge-2:#b7262f; --marine:#1c2541;
  --std:#e3ecfb; --std-ink:#1f3f7a; --lat:#ffe6dd; --lat-ink:#9a3415; --rk:#fff3c9; --rk-ink:#7a5a00; --ligne:#e2e5ee; --r:22px;
  --f:"Outfit",system-ui,"Segoe UI",sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --blanc:#12162a; --gris:#1a1f36; --encre:#eef0f8; --encre-2:#c9cde0; --mute:#9aa0b8; --rouge:#f0616a; --rouge-2:#e04752; --marine:#0d1120;
  --std:#1f2c4d; --std-ink:#bcd0ff; --lat:#4a2318; --lat-ink:#ffc4ad; --rk:#4a3d10; --rk-ink:#ffe08a; --ligne:#2a3150; color-scheme:dark } }
:root[data-theme="dark"]{
  --blanc:#12162a; --gris:#1a1f36; --encre:#eef0f8; --encre-2:#c9cde0; --mute:#9aa0b8; --rouge:#f0616a; --rouge-2:#e04752; --marine:#0d1120;
  --std:#1f2c4d; --std-ink:#bcd0ff; --lat:#4a2318; --lat-ink:#ffc4ad; --rk:#4a3d10; --rk-ink:#ffe08a; --ligne:#2a3150; color-scheme:dark }
*{box-sizing:border-box} html{scroll-behavior:smooth} @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--blanc);color:var(--encre);font-family:var(--f);font-size:1.0625rem;line-height:1.6}
img{max-width:100%;display:block} a{color:var(--rouge)} a:hover{color:var(--rouge-2)}
:focus-visible{outline:3px solid var(--rouge);outline-offset:3px}
h1,h2,h3{font-weight:700;line-height:1.08;margin:0;text-wrap:balance;letter-spacing:-.015em}
h2{font-size:clamp(2rem,4.2vw,3rem)} h3{font-size:1.3rem} p{margin:0}
.wrap{max-width:74rem;margin-inline:auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.eyebrow{display:inline-block;font-size:.8rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--rouge);background:color-mix(in srgb,var(--rouge) 10%,transparent);padding:.3rem .7rem;border-radius:999px}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.85rem 1.4rem;border-radius:999px;font-weight:700;text-decoration:none;border:2px solid transparent;font-size:1rem;line-height:1;cursor:pointer;font-family:var(--f)}
.btn-primary{background:var(--rouge);color:#fff} .btn-primary:hover{background:var(--rouge-2);color:#fff}
.btn-ghost{background:transparent;color:var(--encre);border-color:var(--ligne)} .btn-ghost:hover{border-color:var(--encre)}
.btn-dark{background:var(--encre);color:var(--blanc)} .btn-dark:hover{opacity:.9}
/* header */
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--blanc)}
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:color-mix(in srgb,var(--blanc) 90%,transparent);backdrop-filter:blur(8px)}
.site-header .wrap{display:flex;align-items:center;gap:1rem;min-height:76px}
.brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;color:var(--encre);margin-right:auto;font-weight:700;font-size:1.15rem}
.brand .swallow{width:38px;height:auto;fill:var(--rouge)}
.site-nav ul{list-style:none;margin:0;padding:.3rem;display:flex;gap:.2rem;background:var(--gris);border-radius:999px}
.site-nav a{display:block;color:var(--encre);text-decoration:none;font-weight:600;font-size:.92rem;padding:.5rem .9rem;border-radius:999px} .site-nav a:hover{background:var(--blanc)}
.menu-btn{display:none;background:var(--gris);border:0;color:var(--encre);border-radius:999px;padding:.6rem .95rem;font:inherit;font-weight:700;cursor:pointer}
@media (max-width:960px){.site-nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--blanc);border-bottom:1px solid var(--ligne);padding:1rem max(16px,env(safe-area-inset-left,0px)) 1.25rem}
 .site-nav.open{display:block} .site-nav ul{flex-direction:column;gap:.2rem;border-radius:var(--r)} .menu-btn{display:inline-block} .header-cta{display:none}}
/* hero */
.hero{padding-block:2.5rem 4rem;position:relative;overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}
.hero h1{font-size:clamp(2.9rem,6.5vw,5.2rem)}
.hero h1 span{color:var(--rouge)}
.hero .lead{font-size:1.2rem;color:var(--encre-2);max-width:30em;margin-top:1.25rem} .hero .lead b{color:var(--encre)}
.hero .ctas{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.75rem}
.collage{position:relative;display:grid;grid-template-columns:1.2fr .8fr;grid-template-rows:auto auto;gap:.9rem;max-width:100%}
.collage figure{margin:0;position:relative;overflow:hidden;border-radius:var(--r)} .collage img{width:100%;height:100%;object-fit:cover}
.collage .a{grid-row:1/3;aspect-ratio:4/5;border-radius:var(--r) var(--r) var(--r) 120px}
.collage .b{aspect-ratio:1;border-radius:50% 50% var(--r) var(--r)} .collage .c{aspect-ratio:1;border-radius:var(--r) 120px var(--r) var(--r)}
.collage .sticker{position:absolute;left:-6px;top:14px;transform:rotate(-8deg);background:var(--rk);color:var(--rk-ink);font-weight:800;padding:.6rem .95rem;border-radius:14px;font-size:.95rem;line-height:1.1;box-shadow:0 8px 24px -12px rgba(0,0,0,.35);z-index:1}
.hero .bigbird{position:absolute;right:-6%;top:-10%;width:52vw;max-width:720px;fill:var(--gris);z-index:-1;pointer-events:none}
.tag{position:absolute;left:10px;bottom:10px;background:rgba(28,37,65,.7);color:#fff;font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;padding:.3rem .5rem;border-radius:999px}
@media (max-width:960px){.hero .wrap{grid-template-columns:1fr} .collage{max-width:460px} .hero .bigbird{width:90vw;right:-30%;top:auto;bottom:-10%}}
/* pratique */
.pratique .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.cell{background:var(--gris);border-radius:var(--r);padding:1.5rem} .cell .eyebrow{background:var(--blanc)}
.cell h3{font-size:1.5rem;margin:.6rem 0 .3rem} .cell p{color:var(--encre-2);font-size:.98rem}
@media (max-width:960px){.pratique .wrap{grid-template-columns:1fr}}
section{padding-block:4.5rem}
.sec-head{max-width:40em;margin-bottom:2rem} .sec-head h2{margin-top:.8rem} .sec-head p{color:var(--encre-2);margin-top:.75rem;font-size:1.08rem}
/* danses */
.fams{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.fam{border-radius:var(--r);padding:1.5rem;background:var(--gris)}
.fam.standard{background:var(--std);color:var(--std-ink)} .fam.latine{background:var(--lat);color:var(--lat-ink)} .fam.rock{background:var(--rk);color:var(--rk-ink)}
.fam h3{font-size:1.1rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.9rem;font-weight:800}
.chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}
.chip{background:color-mix(in srgb,var(--blanc) 70%,transparent);padding:.45rem .9rem;border-radius:999px;font-weight:600;font-size:1.05rem;color:inherit}
@media (max-width:960px){.fams{grid-template-columns:1fr}}
/* cours */
.cours{background:var(--gris)} .cours .cols{display:grid;grid-template-columns:1.15fr .85fr;gap:1.5rem;align-items:start}
.agenda{background:var(--blanc);border-radius:var(--r);padding:1.75rem}
.table{width:100%;border-collapse:collapse} .table th,.table td{text-align:left;padding:.95rem .4rem;border-bottom:1px solid var(--ligne);vertical-align:top}
.table th{font-weight:700;font-size:1.1rem;white-space:nowrap} .table .num{font-variant-numeric:tabular-nums;font-weight:800;color:var(--rouge);white-space:nowrap} .table .note{color:var(--mute);font-size:.95rem}
.tarif{background:var(--encre);color:var(--blanc);border-radius:var(--r);padding:1.75rem} .tarif .eyebrow{background:rgba(255,255,255,.12);color:#fff}
.tarif .prix{font-size:3.6rem;font-weight:800;line-height:1;margin-top:.8rem;letter-spacing:-.03em} .tarif .prix small{display:block;font-size:.95rem;font-weight:500;opacity:.8;margin-top:.3rem;letter-spacing:0}
.tarif ul{margin:1.1rem 0 0;padding-left:1.1rem;opacity:.9} .tarif li{margin:.35rem 0}
.gratuit{margin-top:1.2rem;background:var(--rk);color:var(--rk-ink);padding:.9rem 1.1rem;border-radius:14px;font-weight:600}
.salle{display:flex;gap:1rem;align-items:center;margin-top:1rem;padding:1rem;border-radius:var(--r);background:var(--blanc)} .salle img{width:104px;height:76px;object-fit:cover;border-radius:12px;flex:none} .salle b{display:block}
@media (max-width:960px){.cours .cols{grid-template-columns:1fr} .table .note{display:none}}
/* calendrier */
.events{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.ev{display:flex;gap:1rem;align-items:flex-start;padding:1.25rem;border-radius:var(--r);background:var(--gris)}
.ev .date{flex:none;width:4rem;aspect-ratio:1;border-radius:16px;background:var(--rouge);color:#fff;display:grid;place-content:center;text-align:center;line-height:1;font-variant-numeric:tabular-nums}
.ev .date b{font-size:1.6rem;font-weight:800;display:block} .ev .date span{font-size:.62rem;text-transform:uppercase;letter-spacing:.06em;opacity:.9}
.ev h3{font-size:1.15rem} .ev p{color:var(--encre-2);font-size:.93rem;margin-top:.3rem}
.ev-note{margin-top:1.25rem;color:var(--mute)}
@media (max-width:960px){.events{grid-template-columns:1fr}}
/* prof */
.prof .card{display:grid;grid-template-columns:.7fr 1.3fr;gap:0;background:var(--gris);border-radius:var(--r);overflow:hidden}
.prof .portrait{aspect-ratio:4/5;min-height:100%} .prof .portrait img{width:100%;height:100%;object-fit:cover;object-position:top}
.prof .txt{padding:2.25rem} .prof .paras p{margin-top:1rem;color:var(--encre-2)} .prof .paras p:first-child{margin-top:0}
.titres{list-style:none;padding:0;margin:1.5rem 0 0;display:flex;flex-wrap:wrap;gap:.5rem} .titres li{font-size:.85rem;font-weight:600;background:var(--blanc);padding:.4rem .75rem;border-radius:999px}
.liens{margin-top:1.25rem;color:var(--mute);font-size:.98rem}
@media (max-width:960px){.prof .card{grid-template-columns:1fr} .prof .portrait{aspect-ratio:4/3} .prof .txt{padding:1.5rem}}
/* galerie */
.photos{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem}
.ph{margin:0} .ph img{aspect-ratio:1;object-fit:cover;width:100%;border-radius:var(--r)} .ph:nth-child(2) img{border-radius:50% 50% var(--r) var(--r)} .ph:nth-child(3) img{border-radius:var(--r) var(--r) 50% 50%}
.ph figcaption{font-size:.8rem;color:var(--mute);margin-top:.5rem}
@media (max-width:960px){.photos{grid-template-columns:repeat(2,1fr)}}
/* bas */
.bas{background:var(--gris)} .bas .grid{display:grid;grid-template-columns:1fr 1.4fr;gap:1.5rem;align-items:start}
.panel{background:var(--blanc);border-radius:var(--r);padding:1.75rem}
.comite ul{list-style:none;padding:0;margin:1.25rem 0 0} .comite li{display:flex;justify-content:space-between;gap:1rem;padding:.8rem 0;border-bottom:1px solid var(--ligne)} .comite .role{color:var(--mute)} .comite .who{font-weight:700}
.coord{list-style:none;padding:0;margin:1.25rem 0 1.25rem;display:grid;gap:.6rem} .coord b{display:inline-block;min-width:6.5rem;color:var(--mute);font-size:.85rem;text-transform:uppercase;letter-spacing:.04em}
.form{display:grid;gap:1rem} .form label{display:grid;gap:.35rem;font-weight:600;font-size:.95rem}
.form input,.form textarea{font:inherit;padding:.75rem .9rem;border:2px solid var(--ligne);border-radius:14px;background:var(--gris);color:var(--encre);width:100%;min-width:0} .form input:focus,.form textarea:focus{border-color:var(--rouge);outline:none}
.form .row2{display:grid;grid-template-columns:1fr 1fr;gap:1rem} .form-note{font-size:.85rem;color:var(--mute)} .form-ok{padding:.9rem 1rem;border-radius:14px;background:var(--rk);color:var(--rk-ink);font-size:.95rem}
@media (max-width:960px){.bas .grid{grid-template-columns:1fr} .form .row2{grid-template-columns:1fr}}
footer{padding-block:2.5rem;font-size:.95rem;color:var(--mute)}
footer .wrap{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:2rem}
footer ul{list-style:none;margin:0;padding:0;display:grid;gap:.45rem} footer a{color:var(--encre);text-decoration:none} footer a:hover{color:var(--rouge)}
.afcd{display:flex;align-items:center;gap:.75rem;margin-top:.75rem} .afcd img{width:72px;background:#fff;border-radius:10px;padding:4px}
.social{display:flex;align-items:center;gap:.6rem;margin-top:.75rem} .soc{width:36px;height:36px;background:var(--gris);border-radius:50%;display:grid;place-items:center;color:var(--mute)} .soc svg{width:18px;height:18px} .social small{font-size:.8rem}
.maquette{margin-top:2rem;font-size:.8rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
@media (max-width:960px){footer .wrap{grid-template-columns:1fr}}
'''


def render_v3(artifact=False):
    S = SITE
    body = f'''
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="#top">{SWALLOW}<span>{e(S["court"])}</span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="site-nav" id="nav" aria-label="Navigation principale"><ul>{nav_links()}</ul></nav>
    <a class="btn btn-primary header-cta" href="#contact">1er cours gratuit</a>
  </div>
</header>
<main id="top">
<section class="hero">
  <svg class="bigbird" viewBox="0 0 120 80" aria-hidden="true"><path d="M4 30c14-10 32-12 48-6 10-10 26-18 46-18-10 6-18 14-22 24 8 4 18 12 26 28-10-8-20-13-30-15-4 8-10 16-20 24 2-8 3-15 2-22-12 4-26 2-50-15z"/></svg>
  <div class="wrap">
    <div>
      <span class="eyebrow">Danses de couple à Couthuin &amp; Héron</span>
      <h1 style="margin-top:1rem">Venez apprendre <span>à danser</span></h1>
      <p class="lead">{e(ACCROCHE)} <b>{e(GRATUIT)}</b></p>
      <div class="ctas"><a class="btn btn-primary" href="#cours">Info sur les cours</a><a class="btn btn-ghost" href="#calendrier">Les évènements</a></div>
    </div>
    <div class="collage">
      <span class="sticker">1er cours<br>gratuit</span>
      <figure class="a"><img src="assets/placeholders/cours-groupe.jpg" alt="Des couples de danseurs adultes pendant un cours collectif"><span class="tag">{e(PLACEHOLDER)}</span></figure>
      <figure class="b"><img src="assets/placeholders/tango-arcades.jpg" alt="Un couple danse le tango sous des arcades"><span class="tag">{e(PLACEHOLDER)}</span></figure>
      <figure class="c"><img src="assets/placeholders/couple-soiree.jpg" alt="Un couple danse lors d'une soirée"><span class="tag">{e(PLACEHOLDER)}</span></figure>
    </div>
  </div>
</section>
<div class="pratique"><div class="wrap">
  <div class="cell"><span class="eyebrow">Quand</span><h3>Le vendredi soir</h3><p>Débutants à 19h30, perfectionnement à 20h30. Répétition le mercredi à 20h00.</p></div>
  <div class="cell"><span class="eyebrow">Où</span><h3>{e(S["salle"])}</h3><p>{e(S["rue"])}, {e(S["ville"])} · <a href="{S["maps"]}" target="_blank" rel="noopener">itinéraire</a></p></div>
  <div class="cell"><span class="eyebrow">Combien</span><h3>{e(S["cotisation"])} par personne</h3><p>et par cours, pour la saison {e(S["saison"])}. Le premier cours est gratuit.</p></div>
</div></div>

<section class="danses" id="danses"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Ce que nous dansons</span><h2>Neuf danses de couple</h2><p>Le club enseigne la valse lente, la valse viennoise, le tango, le cha-cha, la rumba, le quick step, la samba, le slow fox et le rock.</p></div>
  <div class="fams">{"".join(f'<div class="fam {fam}"><h3>{e(FAMILLES[fam])}</h3><ul class="chips">{"".join(f"<li class=chip>{e(n)}</li>" for n in noms)}</ul></div>' for fam, noms in danses_par_famille().items())}</div>
</div></section>

<section class="cours" id="cours"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Les cours</span><h2>De mi-septembre à mi-avril</h2><p>{e(COURS_INTRO)}</p></div>
  <div class="cols">
    <div>
      <div class="agenda"><table class="table"><thead><tr><th scope="col">Niveau</th><th scope="col">Jour</th><th scope="col">Heure</th><th scope="col"></th></tr></thead><tbody>{bloc_horaires_rows()}</tbody></table>
        <p style="margin-top:1rem;color:var(--encre-2)">{e(COURS_ENCADREMENT)}</p></div>
      <div class="salle"><img src="assets/club/salle-cours.jpg" alt="La salle du Hall Héromnisport pendant un cours"><div><b>{e(S["salle"])}</b>{e(S["rue"])}, {e(S["ville"])}<br><a href="{S["maps"]}" target="_blank" rel="noopener">Ouvrir dans Google Maps</a></div></div>
    </div>
    <div class="tarif"><span class="eyebrow">Tarif</span><p class="prix">{e(S["cotisation"])}<small>par personne et par cours · saison {e(S["saison"])}</small></p>
      <ul>{"".join(f"<li>{e(t)}</li>" for t in TARIFS[1:])}</ul><p class="gratuit">{e(GRATUIT)}</p></div>
  </div>
</div></section>

<section class="calendrier" id="calendrier"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Calendrier</span><h2>Saison {e(S["saison"])}</h2><p>Portes ouvertes, reprise des cours et soirées du club.</p></div>
  <ul class="events">{bloc_evenements()}</ul>
  <p class="ev-note">{e(EVENEMENTS_NOTE)}</p>
</div></section>

<section class="prof" id="professeur"><div class="wrap">
  <div class="card">
    <div class="portrait"><img src="{PROF["photo"]}" alt="Etienne Mine et Martine De Goÿ"></div>
    <div class="txt"><span class="eyebrow">Professeur</span><h2 style="margin-top:.8rem">{e(PROF["nom"])}</h2><p style="color:var(--mute);font-weight:600;margin-top:.2rem">{e(PROF["avec"])}</p>
      <div class="paras" style="margin-top:1.25rem">{"".join(f"<p>{e(p)}</p>" for p in PROF["paras"])}</div>
      <ul class="titres">{bloc_prof_titres()}</ul>
      <p class="liens">Également : {bloc_prof_liens()}</p>
    </div>
  </div>
</div></section>

<section class="galerie" id="galerie"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Galerie</span><h2>La vie du club</h2><p>Dernier cours de la saison 2021-2022 et soirée BBQ du 18 juin 2022.</p></div>
  <div class="photos">{bloc_galerie()}</div>
  <a class="btn btn-dark" style="margin-top:2rem" href="#galerie">Voir toutes les photos</a>
</div></section>

<section class="bas" id="comite"><div class="wrap grid">
  <div class="panel comite"><span class="eyebrow">Le comité</span><h2 style="margin-top:.8rem">Qui fait vivre le club</h2><ul>{bloc_comite()}</ul>
    <p style="margin-top:1.5rem;color:var(--mute);font-size:.95rem">{e(S["asbl"])}, membre de l'<a href="{S["afcd"]}" target="_blank" rel="noopener">AFCD</a>.</p></div>
  <div class="panel" id="contact"><span class="eyebrow">Contact</span><h2 style="margin-top:.8rem">Envie d'essayer ?</h2>
    <ul class="coord">
      <li><b>GSM</b> <a href="{S["tel_href"]}">{e(S["tel"])}</a> <span style="color:var(--mute)">({e(S["tel_note"])})</span></li>
      <li><b>E-mail</b> <a href="mailto:{S["email"]}">{e(S["email"])}</a></li>
      <li><b>Adresse</b> {e(S["salle"])}, {e(S["rue"])}, {e(S["ville"])}</li>
    </ul>
    {contact_form("v3")}
  </div>
</div></section>
</main>
<footer><div class="wrap">
  <div><b style="color:var(--encre);font-size:1.2rem">{e(S["asbl"])}</b>
    <div class="afcd"><img src="assets/club/afcd.png" alt="AFCD"><span>fait partie de l'<a href="{S["afcd"]}" target="_blank" rel="noopener">AFCD</a></span></div>
    {social_slots()}</div>
  <ul>{nav_links()}</ul>
  <ul><li><a href="#contact">Mentions légales (à rédiger)</a></li><li><a href="{S["maps"]}" target="_blank" rel="noopener">Plan d'accès</a></li><li class="maquette">Maquette V3 « Hirondelle »</li></ul>
</div></footer>'''
    fonts = "family=Outfit:wght@400;600;700;800"
    return wrap("Aronde Dance Club · V3 Hirondelle", fonts, V3_CSS, body, artifact)


VARIANTS = {"v1-salon": render_v1, "v2-soiree": render_v2, "v3-hirondelle": render_v3}

if __name__ == "__main__":
    art_dir = None
    if "--artifact" in sys.argv:
        art_dir = Path(sys.argv[sys.argv.index("--artifact") + 1])
        art_dir.mkdir(parents=True, exist_ok=True)
    for name, fn in VARIANTS.items():
        (HERE / f"{name}.html").write_text(fn(False), encoding="utf-8")
        if art_dir:
            (art_dir / f"{name}.html").write_text(fn(True), encoding="utf-8")
        print("ok", name)
