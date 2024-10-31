from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Daten laden
try:
    data_path = "./app/data/dataset.csv"
    df = pd.read_csv(data_path)
    logger.info(f"Erfolgreich {len(df)} Kundendatensätze geladen")
except Exception as e:
    logger.error(f"Fehler beim Laden der Kundendaten: {e}")
    df = pd.DataFrame()  # Leerer DataFrame als Fallback

@app.get("/customers/")
def get_all_customers():
    """Alle Kundendaten abrufen"""
    return df.to_dict(orient="records")

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    """Einzelne Kundendaten basierend auf der ID abrufen"""
    customer = df[df["customer_id"] == customer_id]
    if customer.empty:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return customer.to_dict(orient="records")[0]

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
    
    return filtered_df.to_dict(orient="records")

@app.get("/customers/stats/summary")
def get_customer_stats():
    """Allgemeine Kundenstatistiken"""
    return {
        "total_customers": len(df),
        "average_age": df["age"].mean(),
        "total_revenue": df["total_spent"].sum(),
        "average_revenue_per_customer": df["total_spent"].mean()
    }
