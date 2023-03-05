# Author: Emsii 
# Date: 28.02.2023 
# https://github.com/EmsiiDiss

from asyncio.windows_events import NULL
import sqlite3, traceback, datetime,time
from tabulate import tabulate

class pomoc:    
    def data_rejestracji():
        data_rejestracji = datetime.date.today()
        print ("Data rejestracji...",data_rejestracji)
        return data_rejestracji

    def tables():
        try:
            global connect
            connect = sqlite3.connect('Woda.db', check_same_thread=3)
            connect.execute("""
                CREATE TABLE IF NOT EXISTS MIASTA (
                    id INTEGER PRIMARY KEY ASC,
                    MIASTO varchar(250) NOT NULL
                )""")   
            connect.execute("""
                CREATE TABLE IF NOT EXISTS ORGANIZACJE (
                    id INTEGER PRIMARY KEY ASC,
                    ORGANIZACJA varchar(250) NOT NULL
                )""")        
            connect.executescript("""
                CREATE TABLE IF NOT EXISTS MIEJSCA (
                    id INTEGER PRIMARY KEY ASC,
                    DATA DATE NOT NULL,
                    MIASTO_id INTEGER NOT NULL,
                    ORGANIZACJA_id INTEGER NOT NULL,
                    STAWKA FLOAT NOT NULL,
                    FOREIGN KEY(ORGANIZACJA_id) REFERENCES ORGANIZACJE(id),
                    FOREIGN KEY(MIASTO_id) REFERENCES MIASTA(id)
                )""")
            #connect.execute("DROP TABLE IF EXISTS GRAFIK")
            connect.execute("""
                CREATE TABLE IF NOT EXISTS GRAFIK (
                    id INTEGER PRIMARY KEY ASC,
                    DATA DATE NOT NULL,
                    ZMIANA_id INT NOT NULL,
                    FOREIGN KEY(ZMIANA_id) REFERENCES ZMIANY(id)
                )""")
            connect.execute("""
                CREATE TABLE IF NOT EXISTS ZMIANY (
                    id INTEGER PRIMARY KEY ASC,
                    MIEJSCE_id INTEGER NOT NULL,
                    ZMIANA INT NOT NULL,
                    GODZINA_START TIME NOT NULL,
                    GODZINA_STOP TIME NOT NULL,
                    CZAS varchar(250) NOT NULL,
                    FOREIGN KEY(MIEJSCE_id) REFERENCES MIEJSCA(id)
                )""")
            connect.execute("DROP TABLE IF EXISTS A_Grafik")
            connect.execute("""
                CREATE TABLE IF NOT EXISTS A_Grafik (
                    id INTEGER PRIMARY KEY ASC,
                    DataPracy DATE NOT NULL,
                    Miasto varchar(250) NOT NULL,
                    Organizacja varchar(250) NOT NULL,
                    ZMIANA varchar(250) NOT NULL,
                    Godzina_Rozpoczecia varchar(250) NOT NULL,
                    Godzina_konca varchar(250) NOT NULL,
                    Stawka varchar(250) NOT NULL,
                    Czas varchar(250) NOT NULL,
                    Zarobek varchar(250) NOT NULL
                )""")
                                        
            print ("Table creating successfully")
        except:
            print("\n\nCRASH Table creating\n\n")
            traceback.print_exc()
            raise SystemExit(0) 

class dodaj:
    def organizacja():
        global organizacje_tab
        wyswietl.organizacje()
        organizacja = str(input("Index organizacji...\n     Brak? Wpisz 0 i ją dodaj \n"))
        if organizacja == "0":
            organizacja = str(input("Nazwa organizacji...\n"))
            organizacje_tab.append(organizacja)
            connect.execute('INSERT INTO ORGANIZACJE VALUES(NULL, ?)', (organizacja,))
            organizacje_index = len(organizacje_tab)
        elif organizacja == "n":
            main()
        else:
            organizacje_index = organizacja
        return organizacje_index    

    def miasto():
        global miasta_tab
        wyswietl.miasta()
        miasto = str(input("Index miasta pracy...\n     Brak? Wpisz 0, aby je dodać \n      Wpisz 'n', aby wyjść\n"))
        if miasto == "0":
            miasto = str(input("Miasto pracy...\n"))
            miasta_tab.append(miasto)
            connect.execute('INSERT INTO MIASTA VALUES(NULL, ?)', (miasto,))
            miasta_index = len(miasta_tab)
        elif miasto == "n":
            main()
        else:
            miasta_index = miasto
        return miasta_index

    def stawka():
        stawka = str(input("Stawka...\n"))
        return stawka

    def miejsce():
        global miejsca_tab
        wyswietl.miejsca()
        miejsce = str(input("Index miejsca pracy...\n     Brak? Wpisz 0, aby je dodać \n      Wpisz 'n', aby wyjść\n"))
        if miejsce == "0":
            miejsca_tab.append(miejsce)
            connect.execute('INSERT INTO MIEJSCA VALUES(NULL, ?, ?, ?, ?)', (pomoc.data_rejestracji(), dodaj.miasto(), dodaj.organizacja(), dodaj.stawka(),))
            miejsca_index = len(miejsca_tab)
        elif miejsce == "n":
            main()
        else:
            miejsca_index = miejsce
        return miejsca_index

    def zmiana():
        print(wyswietl.zmiany())
        zmiany = str(input("Index zmiany...\n     Brak? Wpisz 0, aby je dodać \n       Wpisz 'n', aby wyjść\n"))
        if zmiany == "0":
            zmiana = input("Która to zmiana?\n")
            godzina_start = int(input("Godzina rozpoczęcia... "))
            godzina_stop = int(input("Godzina końca... "))
            czas = godzina_stop - godzina_start
            if godzina_start >= 0 and godzina_start <= 9:
                godzina_start = "0" + str(godzina_start) + ":00:00"
            else:
                godzina_start = str(godzina_start) + ":00:00"
            if godzina_stop >= 0 and godzina_stop <= 9:
                godzina_stop = "0" + str(godzina_stop) + ":00:00"
            else:
                godzina_stop = str(godzina_stop) + ":00:00"    
            connect.execute('INSERT INTO ZMIANY VALUES(NULL, ?, ?, ?, ?, ?)', (dodaj.miejsce(), zmiana, godzina_start, godzina_stop, czas,))
        elif zmiany == "n":
            main()    

class wyswietl:
    def miasta():
        global miasta_tab
        cursor = connect.execute("SELECT id, MIASTO from MIASTA")
        organizacje = cursor.fetchall()
        columns=["id","Miasto"]
        for row in organizacje:
            miasta_tab.append((row[0], row[1]))
        print(tabulate(miasta_tab, showindex=False, headers=columns, tablefmt="fancy_grid", numalign="right"))

    def grafik():
        global grafik_tab
        cursor = connect.execute(
        """
        SELECT GRAFIK.id, GRAFIK.DATA, MIASTO, ORGANIZACJA, ZMIANA, GODZINA_START, GODZINA_STOP, STAWKA, Czas  from GRAFIK,ZMIANY,MIEJSCA,MIASTA,ORGANIZACJE
        WHERE GRAFIK.ZMIANA_id=ZMIANY.id and ZMIANY.MIEJSCE_id=MIEJSCA.id and MIEJSCA.MIASTO_id=MIASTA.id AND MIEJSCA.ORGANIZACJA_id=ORGANIZACJE.id
        """)
        #connect.execute('INSERT INTO GRAFIK VALUES(NULL, ?, ?, ?)', ("2023-05-12","5","23",))
        grafiki = cursor.fetchall()
        columns=["id","Data pracy","Miasto","Organizacja", "ZMIANA","Godzina rozpoczęcia","Godzina końca","$/h","Czas","$"]
        #grafik_tab.append(()
        for row in grafiki:
            zarobek=float(row[8])*float(row[7])
            grafik_tab.append((row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],zarobek))
            try:
                connect.execute('INSERT INTO A_Grafik VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],zarobek))
            except sqlite3.IntegrityError:
                pass
        print(tabulate(grafik_tab, showindex=False, headers=columns, tablefmt="fancy_grid", numalign="center"))
        time.sleep(.01)
        grafik_tab = []

    def organizacje():
        global organizacje_tab
        cursor = connect.execute("SELECT id, ORGANIZACJA from ORGANIZACJE")
        organizacje = cursor.fetchall()
        columns=["id","Organizacja"]
        for row in organizacje:
            organizacje_tab.append((row[0], row[1]))
        print(tabulate(organizacje_tab, showindex=False, headers=columns, tablefmt="fancy_grid", numalign="right"))

    def zmiany():
        global zmiany_tab
        cursor = connect.execute(
            """
            SELECT ZMIANY.id, MIASTO, ORGANIZACJA, ZMIANA, GODZINA_START, GODZINA_STOP, CZAS, STAWKA FROM MIEJSCA, ZMIANY, MIASTA, ORGANIZACJE 
            WHERE ZMIANY.MIEJSCE_id=MIEJSCA.id and MIEJSCA.MIASTO_id=MIASTA.id AND MIEJSCA.ORGANIZACJA_id=ORGANIZACJE.id
            """)
        zmiany = cursor.fetchall()
        columns=["id","MIASTO", "Organizacja", "Zmiana", "Godzina startu", "Godzina końca", "Czas pracy"]
        for row in zmiany:
            zmiany_tab.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        print(tabulate(zmiany_tab, showindex=False, headers=columns, tablefmt="fancy_grid", numalign="right"))
        
        

    def miejsca():
        global miejsca_tab
        cursor = connect.execute(
            """
            SELECT MIEJSCA.id,DATA,MIASTO,ORGANIZACJA, STAWKA FROM MIASTA, ORGANIZACJE, MIEJSCA
            WHERE MIEJSCA.MIASTO_id=MIASTA.id AND MIEJSCA.ORGANIZACJA_id=ORGANIZACJE.id
            """)
        miejsca = cursor.fetchall()
        columns=["id","Data dodania","Miasto","Organizacja","Stawka"]
        for row in miejsca:
            miejsca_tab.append((row[0], row[1], row[2], row[3], row[4]))
        print(tabulate(miejsca_tab, showindex=False, headers=columns, tablefmt="fancy_grid", numalign="right"))
        
def start():
    global connect, zmiany_tab, miejsca_tab, organizacje_tab, miasta_tab, grafik_tab
    connect = sqlite3.connect('Woda.db', check_same_thread=3)
    zmiany_tab=[]
    miejsca_tab=[]
    organizacje_tab=[]
    miasta_tab=[]
    grafik_tab = []

def main():
    try:
        global stats
        stats = int(input("""
            Co chcesz zrobić?
                1. Dodanie grafik;
                2. Lista oraz dodanie miejsca pracy;
                3. Lista oraz dodanie organizacji;
                4. Lista oraz dodanie miasta;
                5. Lista oraz dodanie zmian;
            """))
    except ValueError:
        print("To nie liczba...")
        main()    

    if stats == 1:
        wyswietl.grafik()
    elif stats == 2:
        dodaj.miejsce()
    elif stats == 3:
        dodaj.organizacja()
    elif stats == 4:
        dodaj.miasto()
    elif stats == 5:
        dodaj.zmiana()    
    elif stats == 6:
        return
    else:
        main()

    connect.commit() 
    reset=input("Coś jeszcze?  PAC w Enter\n")    
    if reset != "":
        exit()
try:
    pomoc.tables()
    while True:
        start()
        main()

except KeyboardInterrupt:
    print("STOP")
    connect.close()	