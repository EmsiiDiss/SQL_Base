# Author: Emsii 
# Date: 20.05.2024
# https://github.com/EmsiiDiss

import sqlite3, os

lista = []

script_dir = os.path.abspath(os.path.dirname(__file__))

db1_path = os.path.join(script_dir, "Woda.db")
db2_path = os.path.join(script_dir, "Grafik.db")

connect1 = sqlite3.connectect(db1_path)
cursor1 = connect1.cursor()

connect2 = sqlite3.connectect(db2_path)
cursor2 = connect2.cursor()

cursor1.execute("SELECT id, DataPracy, ORGANIZACJA, ZMIANA, Godzina_Rozpoczecia, Godzina_konca, Czas FROM A_Grafik")
rows = cursor1.fetchall()
for row in rows:
    row = list(row)
    if row[3] == "3":
        row[3] = "12"
    lista.append(row)
rows = lista    

for row in rows:
    try:
        cursor2.execute("INSERT INTO GRAFIK (id, DATA, ORGANIZACJA, ZMIANA, Godzina_Rozpoczecia, Godzina_konca, PRZEPRACOWANO) VALUES (?, ?, ?, ?, ?, ?, ?)", row)
    except sqlite3.IntegrityError:
        cursor2.execute("""
            UPDATE GRAFIK
            SET DATA = ?, ORGANIZACJA = ?, ZMIANA = ?, Godzina_Rozpoczecia = ?, Godzina_konca = ?, PRZEPRACOWANO = ?
            WHERE id = ?
            """, (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
        
connect2.commit()
connect1.close()
connect2.close()