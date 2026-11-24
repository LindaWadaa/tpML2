import csv
from collections import Counter
from pathlib import Path

CHEMIN = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"

with open(CHEMIN, encoding="utf-8") as f:
    lignes = list(csv.DictReader(f))

for cat, n in Counter(l["categorie"] for l in lignes).most_common():
    print(f"{cat:<13}{n:>3} {100 * n / len(lignes):>5.1f} % {'#' * n}")

print(f"\nTotal : {len(lignes)} tickets")
print("Tickets ambigus :", sum(int(l["ambigu"]) for l in lignes))
