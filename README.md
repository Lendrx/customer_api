# Customer Insight API

## 🎯 Was macht es?
REST API für die Integration und Analyse von Kundendaten aus verschiedenen Quellen. Machine Learning-basierte Insights für Kundenverhalten und Segmentierung.

## 🛠️ Wie ist es gebaut?
### Tech Stack:
- Python 3.x
- FastAPI
- SQLAlchemy
- Scikit-learn
- Redis

### Architektur-Highlights:
1. Microservice-Architektur
2. Real-time ML-Scoring Pipeline
3. Automatische API-Dokumentation

## 📊 Technische Features
```python
def calculate_customer_score(customer_data):
    features = ['purchase_frequency', 'avg_order_value', 'support_tickets']
    X = customer_data[features]
    return clf.predict_proba(X)[:, 1]
```

Key Features:
- Automatische Kundensegmentierung
- Predictive Analytics
- Real-time Scoring