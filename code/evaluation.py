import sys

sys.stdout.reconfigure(encoding="utf-8")

CATEGORIES = ["facturation", "technique", "compte", "commercial"]


def accuracy(vrais, predits):
    return sum(1 for v, p in zip(vrais, predits) if v == p) / len(vrais)


def scores_par_classe(vrais, predits, classes=CATEGORIES):
    resultat = {}
    for c in classes:
        vp = sum(1 for v, p in zip(vrais, predits) if v == c and p == c)
        fp = sum(1 for v, p in zip(vrais, predits) if v != c and p == c)
        fn = sum(1 for v, p in zip(vrais, predits) if v == c and p != c)
        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) else 0.0)
        resultat[c] = {"precision": precision, "recall": recall,
                       "f1": f1, "support": vp + fn}
    return resultat


def f1_macro(scores):
    return sum(d["f1"] for d in scores.values()) / len(scores) if scores else 0.0


def taux_invalides(predits):
    if not predits:
        return 0.0
    return sum(1 for p in predits if p not in CATEGORIES) / len(predits)


def matrice_confusion(vrais, predits):
    colonnes = CATEGORIES + ["invalide"]
    matrice = {v: {c: 0 for c in colonnes} for v in CATEGORIES}
    for v, p in zip(vrais, predits):
        if v in matrice:
            colonne = p if p in colonnes else "invalide"
            matrice[v][colonne] += 1
    return matrice


def afficher_rapport(etiquette, vrais, predits):
    scores = scores_par_classe(vrais, predits)
    matrice = matrice_confusion(vrais, predits)
    resume = {
        "etiquette": etiquette,
        "n": len(vrais),
        "accuracy": accuracy(vrais, predits),
        "macro_f1": f1_macro(scores),
        "invalides": taux_invalides(predits),
        "scores": scores,
        "matrice": matrice,
    }

    print(f"=== {etiquette} ===")
    print(f"accuracy : {resume['accuracy']:.3f}")
    print(f"macro-F1 : {resume['macro_f1']:.3f}")
    print(f"invalides : {resume['invalides']:.3f}")
    print(f"\n{'categorie':<13}{'precision':>10}{'recall':>8}{'f1':>7}{'n':>5}")
    for categorie, d in scores.items():
        print(f"{categorie:<13}{d['precision']:>10.3f}{d['recall']:>8.3f}"
              f"{d['f1']:>7.3f}{d['support']:>5}")

    colonnes = CATEGORIES + ["invalide"]
    print("\nMatrice de confusion (lignes = vérité, colonnes = prédiction)")
    print(f"{'':<13}" + "".join(f"{c[:6]:>8}" for c in colonnes))
    for vrai in CATEGORIES:
        print(f"{vrai:<13}" + "".join(f"{matrice[vrai][c]:>8}" for c in colonnes))
    return resume
