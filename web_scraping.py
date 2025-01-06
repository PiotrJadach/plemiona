from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import datetime

URL = 'https://pl.twstats.com/pl209/index.php?page=rankings&mode=players&searchstring=&pn='


today = datetime.date.today().strftime("%Y%m%d")
table_name = f"a{today}"

db = psycopg2.connect(dbname="plemiona", user="plemiona_user", password="jLmoubil9es2qzVLMyGIaOvwYrV4ZI27", host="dpg-ctre52lsvqrc73d5hqdg-a.frankfurt-postgres.render.com", port="5432")

cursor = db.cursor()

cursor.execute(f"""
        CREATE TABLE {table_name} 
        (
            ranking INT , 
            imie TEXT, 
            plemie TEXT, 
            punkty INT, 
            wioski INT, 
            srednio_pkt INT
        )
    """)



def pobranie_stron(number):
    print(f'Pracuje nad stroną {number}')
    global data
    page = get(f'{URL}{number}')
    bs = BeautifulSoup(page.text, 'html.parser')
    # Znajdowanie tabeli i parsowanie danych
    tabela = bs.find('table', class_='widget')
    wiersze = tabela.find_all('tr')

    for wiersz in wiersze:
        kolumny = wiersz.find_all('td')
        kolumny = [ele.text.strip() for ele in kolumny]
        data.append(kolumny)


data = []


# Pobieranie zawartości strony
for strona in range(1, 200):
    pobranie_stron(strona)

df = pd.DataFrame(data, columns=['ranking', 'imie', 'plemie', 'punkty', 'wioski', 'srednio_pkt'])
df = df.dropna(subset=[df.columns[0]])

#cursor.execute(f"INSERT INTO {table_name} VALUES (df.values.tolist())", [])
column_names = ", ".join(df.columns)
query = f"INSERT INTO {table_name} ({column_names}) VALUES ({', '.join(['%s'] * len(df.columns))})"

# Konwersja kolumn na typ liczbowy
df['punkty'] = df['punkty'].astype(str).str.replace(',', '').astype(int)
df['srednio_pkt'] = df['srednio_pkt'].astype(str).str.replace(',', '').astype(int)

# Wstawianie danych do bazy
for row in df.values.tolist():
    cursor.execute(query, row)


db.commit()
db.close()