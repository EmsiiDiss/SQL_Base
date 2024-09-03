# Author: Emsii 
# Date: 26.10.2022 
# https://github.com/EmsiiDiss

from asyncio.windows_events import NULL
import sqlite3, shutil, hashlib, datetime, traceback

def tablica():
    try:
        cursor.execute("DROP TABLE IF EXISTS STATS")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS STATS (
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")

        print ("Table creating successfully")
    except:
        print("\n\nCRASH Table creating\n\n")
        traceback.print_exc()
        raise SystemExit(0) 
            
def stats_calculator():
    min  = 9*10^3
    max = NULL
    sr = NULL
    sr_ind = NULL
    kolej = NULL
    last = NULL
    last_id = 1

    print("Starting calculation")
    cursor = conn.execute("SELECT MAX(data), MAX(godzina) from Temperatura")
    for row in cursor:
        koniec = str(int(row[0][0:4]))  + "-" + str(int(row[0][5:7])) + "-" + str(int(row[0][8:12])) + "-" + str(int(row[1][0:2]))
        koniec_dni = datetime.date(int(row[0][0:4]), int(row[0][5:7]), int(row[0][8:12]))
        teraz = NULL
    cursor = conn.execute("SELECT id, godzina, temp_dot, data FROM temperatura WHERE id='%s'" % last_id)
    for row in cursor: 
        rok = int(row[3][0:4])
        miesiac = int(row[3][5:7])
        dzien = int(row[3][8:12])
        godzina = int(row[1][0:2])
        chwila = datetime.date(rok, miesiac, dzien)
        minelo_start = (koniec_dni - chwila).days + 1
    
    
    while koniec != teraz:
        cursor = conn.execute("SELECT id, godzina, temp_dot, data from temperatura WHERE id>='%s'" % last_id)
        for row in cursor:
            teraz = str(rok) + "-" + str(miesiac) + "-" + str(dzien) + "-" + str(godzina)
            wiersz = str(int(row[3][0:4])) + "-" + str(int(row[3][5:7])) + "-" + str(int(row[3][8:12])) + "-" + str(int(row[1][0:2]))
            local_1 = datetime.datetime(int(row[3][0:4]),int(row[3][5:7]),int(row[3][8:12]),int(row[1][0:2]))
            local_2 = datetime.datetime(rok,miesiac,dzien,godzina)
            if local_1 > local_2:
                break
            if wiersz == teraz:
                if min > float(row[2]):
                    min = float(row[2])
                if max < float(row[2]):
                    max = float(row[2])
                sr = sr + float(row[2])
                sr_ind = sr_ind + 1
                if godzina < 10:
                    days_hour = row[3] + str(" 0" + str(godzina) + ":00:00")
                else:
                    days_hour = row[3] + str(" " + str(godzina) + ":00:00")
        
        godzina = godzina + 1
        if days_hour != last:
            # print(days_hour + ", Min = " + str(min) + ", Max = " + str(max) + ", Sr = " + str(sr/sr_ind)[0:5])
            
            cursor.execute('INSERT INTO STATS VALUES(?, ?, ?, ?);', ((days_hour, str(sr/sr_ind)[0:5], min, max)))    # zastąpić str[] na round
            last = days_hour
            min = 9999
            max = NULL
            sr = NULL
            sr_ind = NULL

        if godzina == 24:
            last_id = last_id + 1
            dzien = dzien + 1
            godzina = 0 
        if miesiac%2 != 0:
            if dzien == 31:
                miesiac = miesiac + 1
                dzien = 1
                last_id = row[0]
        else:
            if dzien == 32:
                last_id = row[0]
                miesiac = miesiac + 1
                dzien = 1    
        if miesiac == 13:
            rok = rok + 1
            miesiac = 1
           
        chwila = datetime.date(rok, miesiac, dzien)
        minelo = (koniec_dni - chwila).days + 1
        procent = str(round(100 - (minelo/minelo_start)*100, 2))
        if kolej != chwila:
            print(procent + "%")
            kolej = chwila
        
    conn.commit()
    print("Calculation successfully")

def main():
    try:
        global cursor, conn, stan
        hex_def()
        conn = sqlite3.connect(way_1)
        cursor = conn.cursor()
        print("Opened database successfully")
    except:
        print("\n\nCRASH Opened database\n\n")
        traceback.print_exc()
        raise SystemExit(0) 

    tablica()
    stats_calculator()
    conn.commit()
    conn.close()
    if hex_dsk != hex_source:
        shutil.copyfile(way_1, way_2)
    print("Done")    

def file_as_bytes(file):
    with file:
        return file.read()

def hex_def():
    try:
        global hex_source,hex_dsk
        print("Dowloading file")
        hex_dsk = (hashlib.md5(file_as_bytes(open(way_1, 'rb'))).hexdigest())
        hex_source = (hashlib.md5(file_as_bytes(open(way_2, 'rb'))).hexdigest()) 
        if hex_dsk != hex_source:
            shutil.copyfile(way_2, way_1)
        print("Downloading succesfully")
    except:
        print("\n\nCRASH dowloading\n\n")
        traceback.print_exc()
        raise SystemExit(0) 

        
def scanner():
    global stan, way_1, way_2
    stan = input("\nPlease enter STAN: \n  0. DEFAULT \n  1. NON DEFAULT\n  2. LIST\n =")
    try:
        stan = int(stan)
    except:
        print("d")
        scanner()
    if stan == 0:
        way_1 = "C:/Users/Lenovo/Desktop/VisualStudio/Heat.db"
        way_2 = "Y:/Heat.db"
    elif stan == 1:
        try:
            way_1 = input("Please enter destiny\n 0 - DEFAULT\n")
        except way_1 == 0:
            way_1 = "C:/Users/Lenovo/Desktop/VisualStudio/Heat.db"
        try:        
            way_2 = input("Please enter source\n 0 - DEFAULT\n")
        except way_2 == 0:
            way_2 = "Y:/Heat.db"    
    else:
        print("\nWTF?! \n REPEAT")
        scanner()

    date1 = datetime.datetime.now() 
    main()
    date2 = datetime.datetime.now()
    czas_minuty = int((date2 - date1).total_seconds()/60)
    czas_sekundy = int((date2 - date1).total_seconds()%60)
    print("Czas obliczen = " + str(czas_minuty) + ":" + str(czas_sekundy))  

try:
    scanner()
except KeyboardInterrupt:
    print("STOP_KIboard")
