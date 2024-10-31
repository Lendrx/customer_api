import pandas as pd
import random

# Definitionen für die künstlich generierten Daten
num_records = 1000  # Anzahl der Datensätze

# Definieren der Listen möglicher Namen und Geschlechter
names = ["John Doe", "Jane Smith", "Bob Brown", "Alice Johnson", "Michael Scott", "Rachel Green", "Ross Geller", 
         "Chandler Bing", "Monica Geller", "Phoebe Buffay", "Joey Tribbiani", "Dwight Schrute", "Pam Beesly", 
         "Jim Halpert", "Angela Martin", "Oscar Martinez", "Stanley Hudson", "Kevin Malone", "Kelly Kapoor", 
         "Ryan Howard"]
genders = ["M", "F"]

# Initialisierung einer Liste zum Speichern der generierten Daten
data = []

# Generierung der Daten
for i in range(1, num_records + 1):
    name = random.choice(names)
    age = random.randint(18, 75)
    gender = random.choice(genders)
    purchase_history = random.randint(1, 20)
    total_spent = round(random.uniform(100, 5000), 2)  # Gesamtbetrag zwischen 100 und 5000

    # Hinzufügen der Daten als neuen Datensatz in die Liste
    data.append([i, name, age, gender, purchase_history, total_spent])

# Erstellen des DataFrames
df = pd.DataFrame(data, columns=["customer_id", "name", "age", "gender", "purchase_history", "total_spent"])

# Speichern als CSV-Datei
output_path = # hier den Pfad ein geben, wo die .csv Datei abgelegt werden soll
df.to_csv(output_path, index=False)

output_path
