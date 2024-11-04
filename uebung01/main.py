import re
import pandas as pd
import matplotlib.pyplot as plt

# Datei-Pfad zur entpackten Datei titles.txt
file_path = 'titles.txt'

# Initialisieren der Variablen
data = []

# Einlesen der Daten aus der Datei titles.txt
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Zeilen dekodieren und anhand von Tabs aufteilen
        line = line.strip().split('\t')
        if len(line) == 3:
            pub_type, year, title = line
            data.append((pub_type, int(year), title))

# Konvertieren der Daten in ein DataFrame
df = pd.DataFrame(data, columns=['Type', 'Year', 'Title'])

# Definieren des Regex-Musters für Titel, die mit einem Einzelwort-Akronym und Doppelpunkt beginnen
acronym_pattern = r'^[A-Z][a-zA-Z]*:\s'

# Filtern der Titel, die dem Muster entsprechen
df['Starts_with_acronym'] = df['Title'].str.match(acronym_pattern)

# Zur weiteren Analyse der Daten: Alle gefilterten Titel ausgeben, sortiert nach Jahr
filtered_titles = df[df['Starts_with_acronym']].sort_values(by='Year')[['Year', 'Title']]
print("Gefilterte Titel (nach Jahr sortiert):")
for index, row in filtered_titles.iterrows():
    print(f"{row['Year']}: {row['Title']}")

# Noch mehr Analyse der Daten
overview = df.groupby('Year').agg(
    total_titles=('Title', 'count'),
    filtered_titles=('Starts_with_acronym', 'sum')
).reset_index()
print("\nÜbersicht:")
print("Jahr | Anzahl aller Titel | Anzahl gefilterte Titel")
for index, row in overview.iterrows():
    print(f"{row['Year']} | {row['total_titles']} | {row['filtered_titles']}")


# Berechnen des Anteils der Titel, die mit einem Akronym beginnen, für jedes Jahr
yearly_data = df.groupby('Year')['Starts_with_acronym'].mean().reset_index()

# Part (a) Ausgabe: Anteil der Titel, die mit einem Akronym beginnen, für jedes Jahr
# print("Anteil der Titel, die mit einem Akronym und Doppelpunkt beginnen, pro Jahr:")
# print(yearly_data)

# Diagramm für Part (a) - Speichern als PNG
plt.figure(figsize=(10, 6))
plt.plot(yearly_data['Year'], yearly_data['Starts_with_acronym'], marker='o')
plt.title("Fraction of Titles Starting with an Acronym and Colon Over Time")
plt.xlabel("Year")
plt.ylabel("Fraction of Titles with Acronym Start")
plt.grid()
plt.savefig("akronym_anteil_pro_jahr.png")
plt.close()

# Eine Kopie des gefilterten DataFrames erstellen, um die Warnung zu vermeiden
df_acronym_titles = df[df['Starts_with_acronym']].copy()

# Extrahieren des Texts nach dem Doppelpunkt und Berechnen der Wortanzahl
df_acronym_titles['After_colon_text'] = df_acronym_titles['Title'].str.split(pat=':', n=1).str[1]
df_acronym_titles['Word_count_after_colon'] = df_acronym_titles['After_colon_text'].str.split().str.len()

# Berechnen der Häufigkeit der unterschiedlichen Wortlängen
word_count_freq = df_acronym_titles['Word_count_after_colon'].value_counts().sort_index()

# Ausgabe: Häufigkeit der unterschiedlichen Längen des Texts nach dem Doppelpunkt
print("\nHäufigkeit der Titellängen (in Wörtern) nach dem Doppelpunkt:")
print(word_count_freq)

# Diagramm für Part (b) - Speichern als PNG
plt.figure(figsize=(10, 6))
plt.bar(word_count_freq.index, word_count_freq.values)
plt.title("Frequency of Title Lengths (in Words) After the Colon")
plt.xlabel("Word Count After Colon")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.savefig("wortanzahl_nach_doppelpunkt.png")
plt.close()
