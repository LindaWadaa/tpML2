import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_RESULTATS = RACINE / "resultats"
CHEMIN_TICKETS = RACINE / "data" / "tickets.csv"


def charger_resultats():
    resultats = []
    for chemin in sorted(DOSSIER_RESULTATS.glob("*.json")):
        with open(chemin, encoding="utf-8") as f:
            resultats.append(json.load(f))
    return resultats


def afficher_tableau(resultats):
    print(f"{'candidat':<34}{'acc':>7}{'macro-F1':>10}{'invalid.':>9}{'tickets':>9}")
    for r in sorted(resultats, key=lambda x: x["macro_f1"], reverse=True):
        print(f"{r['etiquette']:<34}{r['accuracy']:>7.3f}"
              f"{r['macro_f1']:>10.3f}{r['invalides']:>9.3f}{r['n']:>9}")

    if len(resultats) >= 2:
        classes = sorted(resultats, key=lambda x: x["macro_f1"], reverse=True)
        premier, deuxieme = classes[0], classes[1]
        ecart = premier["macro_f1"] - deuxieme["macro_f1"]
        points = 100 * ecart
        tickets = round(points / (100 / premier["n"]))
        print(f"\nÉcart 1er / 2e : {points:.1f} points, soit {tickets} ticket(s) sur {premier['n']}.")
        if tickets < 5:
            print("Conclusion : pas de différence mesurable (moins de cinq tickets).")
        else:
            print("Conclusion : différence mesurable (au moins cinq tickets).")


def afficher_divergences(resultats):
    with open(CHEMIN_TICKETS, encoding="utf-8") as f:
        tickets = {l["id"]: l for l in csv.DictReader(f)}

    par_ticket = {}
    for r in resultats:
        for identifiant, prediction in zip(r["ids"], r["predits"]):
            par_ticket.setdefault(identifiant, {})[r["etiquette"]] = prediction

    divergents = 0
    for identifiant, predictions in par_ticket.items():
        if len(set(predictions.values())) < 2:
            continue
        divergents += 1
        ticket = tickets.get(identifiant, {})
        print(f"\n{identifiant} (référence : {ticket.get('categorie', '?')}, ambigu : "
              f"{ticket.get('ambigu', '?')})")
        print(f"  {ticket.get('texte', '')}")
        for etiquette, prediction in predictions.items():
            print(f"    {etiquette:<34} -> {prediction}")

    print(f"\n{divergents} ticket(s) divergent(s) sur {len(par_ticket)}.")


if __name__ == "__main__":
    resultats = charger_resultats()
    if not resultats:
        raise SystemExit("Aucun JSON dans resultats/ : lancez d'abord evaluer.py.")
    afficher_tableau(resultats)
    print("\n--- Tickets sur lesquels les candidats divergent ---")
    afficher_divergences(resultats)
