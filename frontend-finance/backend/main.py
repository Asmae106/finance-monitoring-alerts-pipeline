from fastapi import FastAPI, Query

from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import time, random
from datetime import datetime, timedelta
from typing import List


app = FastAPI()

# Autorisation CORS pour Angular

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stockage en mémoire (limité à 100 entrées)
prix_historique: List[dict] = []
alertes: List[dict] = []

ASSET = "BTC"
PRIX_ACTUEL = 67000.0

@app.get("/alerts")
def get_alerts():
    return alertes[-10:]  # dernières alertes

@app.get("/prices")
def get_prices():
    return prix_historique[-10:]  # derniers prix

def nettoyer_liste(liste: List[dict], taille_max: int = 100):
    """Garder uniquement les N derniers éléments"""
    while len(liste) > taille_max:
        liste.pop(0)

def trouver_prix_il_y_a(prix_historique: List[dict], secondes: int) -> float | None:
    """
    Trouver dans prix_historique le prix correspondant à 'secondes' secondes avant maintenant,
    ou le plus proche avant cette date.
    """
    cible = datetime.utcnow() - timedelta(seconds=secondes)
    # parcourir prix du plus récent au plus ancien
    for prix in reversed(prix_historique):
        t = datetime.fromisoformat(prix["timestamp"])
        if t <= cible:
            return prix["price"]
    return None  # pas trouvé

def simulateur_de_prix():
    global PRIX_ACTUEL
    while True:
        variation = random.uniform(-2, 2)  # ±2%
        nouveau_prix = round(PRIX_ACTUEL * (1 + variation / 100), 2)
        now = datetime.utcnow().isoformat()

        prix_historique.append({
            "asset": ASSET,
            "timestamp": now,
            "price": nouveau_prix
        })
        nettoyer_liste(prix_historique)

        # Trouver prix d'il y a 60 secondes pour alerte
        prix_60s = trouver_prix_il_y_a(prix_historique, 60)
        if prix_60s is not None:
            variation_percent = ((nouveau_prix - prix_60s) / prix_60s) * 100
            if variation_percent <= -10.0:
                alertes.append({
                    "asset": ASSET,
                    "timestamp": now,
                    "variation": round(variation_percent, 2),
                    "price": nouveau_prix
                })
                nettoyer_liste(alertes)
                print(f"⚠️ ALERTE : Variation {variation_percent:.2f}% à {now}")

        PRIX_ACTUEL = nouveau_prix
        print(f"Prix généré : {nouveau_prix} à {now}")

        time.sleep(1)  # toutes les secondes

@app.on_event("startup")
def start_simulation():
    t = Thread(target=simulateur_de_prix, daemon=True)
    t.start()
@app.get("/report")
def get_report(date: str = Query(...)):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Format de date invalide. Format attendu : YYYY-MM-DD"}

    # Filtrer les prix correspondant à la date donnée
    donnees_jour = [
        prix for prix in prix_historique
        if datetime.fromisoformat(prix["timestamp"]).date() == date_obj
    ]

    if not donnees_jour:
        return {
            "date": str(date_obj),
            "total": 0,
            "data": [],
            "stats": {}
        }

    # Statistiques simples (min, max, moyenne, etc.)
    prix_liste = [p["price"] for p in donnees_jour]
    prix_min = min(prix_liste)
    prix_max = max(prix_liste)
    prix_moyen = round(sum(prix_liste) / len(prix_liste), 2)

    return {
        "date": str(date_obj),
        "total": len(donnees_jour),
        "data": donnees_jour,
        "stats": {
            "min": prix_min,
            "max": prix_max,
            "average": prix_moyen
        }
    }
