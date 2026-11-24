from classifieur import CONSIGNE_EXEMPLES
from evaluer import charger, evaluer

MODELE = "openai/gpt-oss-20b"

evaluer(
    MODELE,
    charger(),
    consigne=CONSIGNE_EXEMPLES,
    etiquette=f"{MODELE} + 4 exemples",
)
