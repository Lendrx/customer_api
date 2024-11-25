from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging
import os
from decouple import config

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lade Umgebungsvariablen
DATA_PATH = config("DATA_PATH", default="./app/data/dataset.csv")

app = FastAPI(
    title="KundenInsight Pro",
    description="Intelligente Kundenanalyse-API",
    version="0.1.0"
)

# CORS Middleware für Webkompatibilität
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daten laden mit validem Fallback und präzisem Fehlerhandling
if not os.path.exists(DATA_PATH):
    logger.error(f"Dataset nicht gefunden: {DATA_PATH}")
    raise RuntimeError(f"Dataset nicht gefunden: {DATA_PATH}. Bitte überprüfen.")
try:
    df = pd.read_csv(DATA_PATH)
    logger.info(f"Erfolgreich {len(df)} Kundendatensätze geladen")
except Exception as e:
    logger.error(f"Fehler beim Laden der Kundendaten: {e}")
    raise RuntimeError(f"Fehler beim Laden der Kundendaten: {e}")

# Sicherstellen, dass der DataFrame erwartete Spalten enthält
expected_columns = {"customer_id", "age", "total_spent"}
if not expected_columns.issubset(df.columns):
    raise ValueError(
        f"Fehlende Spalten im Dataset. Erwartet: {expected_columns}. Vorhanden: {set(df.columns)}"
    )

@app.get("/customers/")
def get_all_customers():
    """Alle Kundendaten abrufen"""
    return df.to_dict(orient="records")

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    """Einzelne Kundendaten basierend auf der ID abrufen"""
    try:
        customer = df[df["customer_id"] == customer_id]
        if customer.empty:
            raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
        return customer.to_dict(orient="records")[0]
    except KeyError as e:
        logger.error(f"Fehler bei der Anfrage für Kunden-ID {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Datenverarbeitungsfehler")

@app.get("/customers/segment/{age_group}")
def get_customers_by_age_group(age_group: str):
    """Kundensegmente basierend auf Altersgruppe abrufen"""
    age_groups = {
        "young": (0, 30),
        "middle": (30, 50),
        "senior": (50, 100)
    }
    
    if age_group not in age_groups:
        raise HTTPException(status_code=400, detail="Ungültige Altersgruppe")
    
    min_age, max_age = age_groups[age_group]
    filtered_df = df[(df["age"] >= min_age) & (df["age"] < max_age)]
    
    if filtered_df.empty:
        logger.info(f"Keine Kunden in der Altersgruppe {age_group} gefunden")
        return {"message": f"Keine Kunden in der Altersgruppe {age_group} gefunden"}
    
    return filtered_df.to_dict(orient="records")

@app.get("/customers/stats/summary")
def get_customer_stats():
    """Allgemeine Kundenstatistiken"""
    try:
        total_customers = len(df)
        average_age = df["age"].mean()
        total_revenue = df["total_spent"].sum()
        average_revenue = df["total_spent"].mean()

        if pd.isna(average_age) or pd.isna(average_revenue):
            raise ValueError("Unzureichende Daten für die Berechnung von Statistiken.")

        return {
            "total_customers": total_customers,
            "average_age": average_age,
            "total_revenue": total_revenue,
            "average_revenue_per_customer": average_revenue
        }
    except KeyError as e:
        logger.error(f"Fehlende Daten für Statistiken: {e}")
        raise HTTPException(status_code=500, detail="Fehler bei der Statistikberechnung")
    except Exception as e:
        logger.error(f"Allgemeiner Fehler bei Statistiken: {e}")
        raise HTTPException(status_code=500, detail="Interner Serverfehler")

