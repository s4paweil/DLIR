import re
import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = 'titles.txt'

data = []

# Read data from file
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip().split('\t')
        if len(line) == 3:
            pub_type, year, title = line
            data.append((pub_type, int(year), title))

df = pd.DataFrame(data, columns=['Type', 'Year', 'Title'])

# Regular expression for filtering for acronyms
acronym_pattern = r'^[A-Z][a-zA-Z]*:\s'

# Filtering for acronyms
df['Starts_with_acronym'] = df['Title'].str.match(acronym_pattern)

# Additional output for analysing the data
filtered_titles = df[df['Starts_with_acronym']].sort_values(by='Year')[['Year', 'Title']]
print("Gefilterte Titel (nach Jahr sortiert):")
for index, row in filtered_titles.iterrows():
    print(f"{row['Year']}: {row['Title']}")

overview = df.groupby('Year').agg(
    total_titles=('Title', 'count'),
    filtered_titles=('Starts_with_acronym', 'sum')
).reset_index()
print("\nÜbersicht:")
print("Jahr | Anzahl aller Titel | Anzahl gefilterte Titel")
for index, row in overview.iterrows():
    print(f"{row['Year']} | {row['total_titles']} | {row['filtered_titles']}")



yearly_data = df.groupby('Year')['Starts_with_acronym'].mean().reset_index()

# Chart (a)
plt.figure(figsize=(10, 6))
plt.plot(yearly_data['Year'], yearly_data['Starts_with_acronym'], marker='o')
plt.title("Fraction of Titles Starting with an Acronym and Colon Over Time")
plt.xlabel("Year")
plt.ylabel("Fraction of Titles with Acronym Start")
plt.grid()
plt.savefig("acronym-fraction-per-year.png")
plt.close()

# Copy filtered data
df_acronym_titles = df[df['Starts_with_acronym']].copy()

df_acronym_titles['After_colon_text'] = df_acronym_titles['Title'].str.split(pat=':', n=1).str[1]
df_acronym_titles['Word_count_after_colon'] = df_acronym_titles['After_colon_text'].str.split().str.len()

word_count_freq = df_acronym_titles['Word_count_after_colon'].value_counts().sort_index()

# Output: Word count after colon
print("\nHäufigkeit der Titellängen (in Wörtern) nach dem Doppelpunkt:")
print(word_count_freq)

# Chart (b)
plt.figure(figsize=(10, 6))
plt.bar(word_count_freq.index, word_count_freq.values)
plt.title("Frequency of Title Lengths (in Words) After the Colon")
plt.xlabel("Word Count After Colon")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.savefig("wortanzahl_nach_doppelpunkt.png")
plt.close()
