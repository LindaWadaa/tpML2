# Fiche de décision — Atelier 2

## Tâche et jeu de test
Router les tickets vers quatre équipes (facturation, technique, compte, commercial).
72 tickets annotés, classes déséquilibrées : 22 / 20 / 16 / 14. 7 tickets ambigus.

## Métrique de décision
Macro-F1, choisie avant de voir les résultats, car l'accuracy est aveugle au
déséquilibre : ignorer totalement la catégorie commercial ne coûterait que 19,4 points
d'accuracy, alors qu'aucun client commercial ne serait routé.

## Candidats évalués
Protocole identique pour tous : mêmes 72 tickets, même consigne, même parsing JSON,
température 0, pause de 2,1 s. Durées mesurées sur 72 tickets, pause incluse.

| Candidat | accuracy | macro-F1 | invalides | durée (s) |
|---|---|---|---|---|
| openai/gpt-oss-20b | 0,958 | 0,9574 | 0 | 181,2 |
| openai/gpt-oss-20b + 4 exemples | 0,958 | 0,9571 | 0 | 211,6 |
| qwen/qwen3.8-27b | 0,958 | 0,9559 | 0 | 170,8 |
| openai/gpt-oss-120b | 0,931 | 0,9326 | 0 | 190,5 |

## Modèle retenu et son score
**openai/gpt-oss-20b**, macro-F1 = 0,957 (69 tickets bien routés sur 72).
Il est ex æquo avec qwen/qwen3.8-27b ; à qualité égale, on retient le moins cher
(0,075 $/1M jetons en entrée contre 0,80 $) et le plus rapide d'après le fournisseur
(~1000 jetons/s contre ~450).

## Écart avec le deuxième
En points : 0,04 point (0,9574 contre 0,9571) — En tickets : **0 / 72**.
Écart avec le 120B : 2,5 points, soit environ 2 tickets / 72.
Les deux écarts sont inférieurs au seuil de 5 tickets : pas de différence mesurable.
Le gain du few-shot est lui aussi nul : il corrige T066 (geste commercial → facturation)
mais fait passer T004 en facturation au lieu de commercial.

## Catégorie la plus faible, latence, risque identifié
- Catégorie la plus faible du modèle retenu : **compte**, F1 = 0,938, avec 2 confusions
  dans l'axe compte ↔ technique (T023, T041). Le 120B échoue davantage sur technique
  (recall 0,850) en se laissant tromper par les mots « règlement / paiement » (T039, T061).
- Latence : les durées ci-dessus incluent 151 s de pause et varient selon la longueur des
  réponses ; elles ne départagent pas les modèles. La fiche fournisseur donne 1000 t/s
  pour le 20B, 500 t/s pour le 120B et 450 t/s pour qwen.
- Risque : 7 tickets ambigus sur 72 (9,7 %) et 3 des 6 désaccords entre candidats les
  concernent. Un ticket vaut 1,4 point de macro-F1 : sur un jeu aussi petit, un écart
  de 1 à 2 tickets est du bruit, pas une preuve.

## Décision finale
« openai/gpt-oss-20b obtient 0,957 de macro-F1 sur nos 72 tickets, contre 0,956 pour
qwen et 0,933 pour le 120B ; l'écart n'est pas mesurable (moins de cinq tickets), donc nous
retenons le plus petit modèle, et nos erreurs se concentrent sur la frontière
 compte ↔ technique. »
