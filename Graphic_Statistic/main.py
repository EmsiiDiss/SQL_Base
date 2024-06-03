# Author: Emsii 
# Date: 20.05.2024
# https://github.com/EmsiiDiss


import sqlite3, datetime, os

script_dir = os.path.abspath(os.path.dirname(__file__))

def connect(file):
    connect = sqlite3.connect(file)
    print("Opened database successfully")
    return connect

def tablica(connect, plik, table_name):
    try:
        if plik == "grafik":
            connect.execute("""
                CREATE TABLE IF NOT EXISTS GRAFIK (
                    id INTEGER PRIMARY KEY ASC,
                    DATA varchar(250) NOT NULL,
                    ORGANIZACJA varchar(250) NOT NULL,
                    ZMIANA varchar(250) NOT NULL,
                    Godzina_Rozpoczecia varchar(250) NOT NULL,
                    Godzina_konca varchar(250) NOT NULL,
                    PRZEPRACOWANO varchar(250) NOT NULL
                )""")
            
        elif plik == "stawki":
            # table_names = ["MOSiR", "Paduch"]
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY ASC,
                    DATA varchar(250) NOT NULL,
                    STAWKA varchar(250) NOT NULL
                )
                """
            connect.execute(create_table_query)

        print ("Tables creating successfully")

    except KeyboardInterrupt:
        print("Key Stop")
    connect.commit()

def wszystkie_tablice(connect, plik):
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Zawartość pliku: ", plik)
    for i, table in enumerate(tables):
        print(i+1, table[0])

class cli:
    def edycja_plikow():
        choise = input("Wybierz co chcesz uczynić:\n 1 = edycja pliku Stawki.db\n 2 = edycja pliku Grafik.db\n 0 = wyjscie\n")

        if choise == "1":
            cli.edycja_stawki()

        elif choise == "2":
            cli.edycja_stawki()

        elif choise == "0":
            starter()

        cli.edycja_plikow()

    def edycja_stawki():
            choise = input("Wybierz co chcesz uczynić:\n 1 = edycja pliku Stawki.db\n 2 = wyświetlenie zawartości pliku Stawki.db\n 0 = wyjscie\n")

            if choise == "1": 
                choise = input("Wybierz co chcesz uczynić:\n 1 = dodanie nowej organizacji \n 2 = usunięcie organizacji\n 3 = edycja wartosci stawki w organizacji\n")
                if choise == "1": 
                    tablica(connect(os.path.join(script_dir, "Stawki.db")), "stawki", input("Podaj nazwe nowej tablicy:\n"))
                elif choise == "2":
                    print("delete")
                elif choise == "3":
                    print("edit")

            elif choise == "2":
                wszystkie_tablice(connect(os.path.join(script_dir, "Stawki.db")), "Stawki.db")     

            elif choise == "0":
                cli.edycja_plikow()

            cli.edycja_stawki

    def edycja_grafik():
            choise = input("Wybierz co chcesz uczynić:\n 1 = edycja pliku Grafik.db\n 2 = wyświetlenie zawartości pliku Grafik.db\n 0 = wyjscie\n")

            if choise == "1": 
                choise = input("Wybierz co chcesz uczynić:\n 1 = dodanie nowego dnjia \n 2 = usunięcie dnia\n 3 = edycja dnia\n")

                tablica(connect(os.path.join(script_dir, "Grafik.db")), "grafik", input("Podaj nazwe nowej tablicy"))
            elif choise == "2":
                wszystkie_tablice(connect(os.path.join(script_dir, "Stawki.db")), "Stawki.db")


            elif choise == "0":
                cli.edycja_plikow()

            cli.edycja_grafik()    

def starter():
    tablica(connect(os.path.join(script_dir, "Grafik.db")), "grafik", None)
    choise = input("Chcesz edytować pliki bazy danych? \n 1 = TAK\n 2 = NIE \n")
    if choise == "1":
        cli.edycja_plikow()

    elif choise == "2":
        print( "\n" * 10 + "W takim razie co?" + "\n" * 2)
        starter()
    else:
        SystemExit


try:
    
    starter()


except KeyboardInterrupt:
    print("XDD")        