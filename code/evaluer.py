import csv
import json
import sys
import time
from pathlib import Path

from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport

PAUSE = 2.1
RACINE = Path(__file__).resolve().parent.parent
DOSSIER_RESULTATS = RACINE / "resultats"
CHEMIN_TICKETS = RACINE / "data" / "tickets.csv"


def charger(chemin=CHEMIN_TICKETS):
    with open(chemin, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None):
    etiquette = etiquette or modele
    vrais, predits, debut = [], [], time.time()

    for ligne in lignes:
        predits.append(classer(ligne["texte"], modele, consigne=consigne))
        vrais.append(ligne["categorie"])
        time.sleep(PAUSE)

    resume = afficher_rapport(etiquette, vrais, predits)
    resume.update(
        modele=modele,
        etiquette=etiquette,
        duree_s=round(time.time() - debut, 1),
        predits=predits,
        ids=[l["id"] for l in lignes],
    )

    nom_fichier = etiquette.replace("/", "_").replace(" ", "_") + ".json"
    fichier_sortie = DOSSIER_RESULTATS / nom_fichier
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)
    print(f"\nRésultats enregistrés dans : {fichier_sortie}")
    return resume


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage : python evaluer.py <modele>")
    evaluer(sys.argv[1], charger())
