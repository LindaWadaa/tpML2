import json
import os
import time
from groq import Groq, RateLimitError

CATEGORIES = ["facturation", "technique", "compte", "commercial"]

CONSIGNE = """Tu es un agent de tri du service client.
Classe le ticket dans exactement une catégorie :
- facturation : montant, facture, paiement, remboursement.
- technique : un service ne fonctionne pas comme prévu.
- compte : accès au compte ou données personnelles.
- commercial : choix d'offre, abonnement, résiliation.
Si plusieurs catégories semblent possibles, retiens l'intention
principale du client : ce qu'il veut obtenir.
Réponds uniquement par un objet JSON de la forme
{"categorie": "<une des quatre>"}."""

CONSIGNE_EXEMPLES = CONSIGNE + """
Exemples :
"Le geste commercial promis n'est pas sur mon relevé." ->
{"categorie": "facturation"}
"Je paie chaque mois et rien ne marche depuis jeudi." ->
{"categorie": "technique"}
"Mon associé doit consulter les mêmes documents." ->
{"categorie": "compte"}
"Je déménage à l'étranger en septembre." ->
{"categorie": "commercial"}"""

_client = None


def obtenir_client():
    global _client
    if _client is None:
        cle = os.environ.get("GROQ_API_KEY")
        if not cle:
            raise SystemExit("GROQ_API_KEY absente : exportez-la dans le terminal courant.")
        _client = Groq(api_key=cle)
    return _client


def classer(texte, modele, consigne=CONSIGNE, temperature=0.0):
    for tentative in range(4):
        try:
            reponse = obtenir_client().chat.completions.create(
                model=modele,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": consigne},
                    {"role": "user", "content": texte},
                ],
            )
            break
        except RateLimitError:
            if tentative == 3:
                return "invalide"
            time.sleep(2.1 * (tentative + 1))

    try:
        categorie = json.loads(reponse.choices[0].message.content).get("categorie", "")
    except (json.JSONDecodeError, AttributeError, TypeError):
        return "invalide"
    categorie = str(categorie).strip().lower()
    return categorie if categorie in CATEGORIES else "invalide"
