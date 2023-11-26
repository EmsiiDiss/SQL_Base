# Author: Emsii
# Date: 26.10.2022
# https://github.com/EmsiiDiss

#from asyncio.windows_events import NULL
import sqlite3, shutil, datetime, traceback

def tablica():
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Hours")
        cursor.execute("DROP TABLE IF EXISTS Days")
        cursor.execute("DROP TABLE IF EXISTS Average")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Hours (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Days (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Average (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")
        print ("Tables creating successfully")
    except:
        print("\n\nCRASH Tables creating\n\n")
        traceback.print_exc()
        raise SystemExit(0)

def temp_calculator():
    try:
        print("Calculation END")
    except:
            print("\n\nCRASH Temp Calculation\n\n")
            traceback.print_exc()
            raise SystemExit(0)

def zegar():
    global rok, miesiac, dzien, godzina
    parzyste = [4,6,9,11]

    if godzina == 24:
        dzien = dzien + 1
        godzina = 0

    if miesiac in parzyste:
        if dzien == 31:
            miesiac = miesiac + 1
            dzien = 1
    elif miesiac == 2:
        if rok%4 != 0:
            if dzien == 29:
                miesiac = miesiac + 1
                dzien = 1
        else:
            if dzien == 30:
                miesiac = miesiac + 1
                dzien = 1
    else:
        if dzien == 32:
            miesiac = miesiac + 1
            dzien = 1

    if miesiac == 13:
        rok = rok + 1
        miesiac = 1

def main():
    print("XD")

def download(way_1, way_2):
    try:
        print("Dowloading file")
        shutil.copyfile(way_2, way_1)
        print("Downloading succesfully")
    except:
        print("\n\nCRASH dowloading\n\n")
        traceback.print_exc()
        raise SystemExit(0)

def connect(way_1):
    try:
        global conn
        conn = sqlite3.connect(way_1)
        print("Opened database successfully")

    except:
        print("\n\nCRASH Opened database\n\n")
        traceback.print_exc()
        raise SystemExit(0)

def calculating_temp():
    global rok, miesiac, dzien, godzina
    NULL = 0
    min_h = 1000
    max_h = NULL
    avr_h = NULL
    avr_ind_h = NULL

    min_d = 1000
    max_d = NULL
    avr_d = NULL
    avr_ind_d = NULL

    last_id = 1
    now_h = NULL
    last_day_hour = NULL
    last_day = NULL
    kolej = NULL

    print("Starting calculation")
    cursor = conn.execute("SELECT MAX(data), MAX(godzina) from Temperatura")
    for row in cursor:
        end_h = str(int(row[0][0:4]))  + "-" + str(int(row[0][5:7])) + "-" + str(int(row[0][8:10])) + "-" + str(int(row[1][0:2]))
        end_d = datetime.date(int(end_h[0:4]),int(end_h[5:7]),int(end_h[8:9]))

    cursor = conn.execute("SELECT id, godzina, temp_dot, data FROM temperatura WHERE id='%s'" % last_id)
    for row in cursor:
        rok = int(row[3][0:4])
        miesiac = int(row[3][5:7])
        dzien = int(row[3][8:10])
        godzina = int(row[1][0:2])
        chwila = datetime.date(rok, miesiac, dzien)
        minelo_start = (end_d - chwila).days + 1

    while end_h != now_h:
        cursor = conn.execute("SELECT id, godzina, temp_dot, data from temperatura WHERE id>='%s'" % last_id)
        for row in cursor:
            now_h = str(rok) + "-" + str(miesiac) + "-" + str(dzien) + "-" + str(godzina)
            line_h = str(int(row[3][0:4])) + "-" + str(int(row[3][5:7])) + "-" + str(int(row[3][8:10])) + "-" + str(int(row[1][0:2]))

            now_d = now_h[0:10]
            line_d = line_h[0:10]

            local_1 = datetime.date(int(row[3][0:4]),int(row[3][5:7]),int(row[3][8:10]))
            local_2 = datetime.date(rok,miesiac,dzien)
            if local_1 > local_2:
                break
            if line_h == now_h:
                if min_h > float(row[2]):
                    min_h = float(row[2])
                if max_h < float(row[2]):
                    max_h = float(row[2])
                avr_h = avr_h + float(row[2])

                avr_ind_h = avr_ind_h + 1

                if godzina < 10:
                    days_hour = row[3] + str(" 0" + str(godzina) + ":00:00")
                else:
                    days_hour = row[3] + str(" " + str(godzina) + ":00:00")

            if line_d == now_d:
                if min_d > float(row[2]):
                    min_d = float(row[2])
                if max_d < float(row[2]):
                    max_d = float(row[2])
                avr_d = avr_d + float(row[2])
                avr_ind_d = avr_ind_d + 1

        godzina = godzina + 1
        if days_hour != last_day_hour:
            cursor.execute('INSERT INTO Hours VALUES(NULL, ?, ?, ?, ?);', ((days_hour, str(round(avr_h/avr_ind_h,2)), min_h, max_h)))
            last_day_hour = days_hour
            min_h = 1000
            max_h = NULL
            avr_h = NULL
            avr_ind_h = NULL

            days = days_hour[0:10]
            if days != last_day:
                cursor.execute('INSERT INTO Days VALUES(NULL, ?, ?, ?, ?);', ((days, str(round(avr_d/avr_ind_d,2)), min_d, max_d)))
                last_day = days
                min_d = 1000
                max_d = NULL
                avr_d = NULL
                avr_ind_d = NULL

        if godzina == 24:
            zegar()
            last_id = row[0]

        chwila = datetime.date(rok, miesiac, dzien)
        minelo = (end_d - chwila).days + 1
        procent = round(50 - (minelo/minelo_start)*50,2)
        if kolej != chwila:
            print(str(procent) + "%")
            kolej = chwila

    print("Temp Calculation successfully")

def calculating_avg():
    NULL = 0
    min_avg = NULL
    max_avg = NULL
    avr_avg = NULL
    avr_ind = NULL

    last_id = 1
    now_h = NULL
    kolej = NULL

    print("Starting calculation Average Temp")
    cursor = conn.execute("SELECT MAX(data) from Hours")
    for row in cursor:
        end_d = str(row[0])[0:10]
        end_day = datetime.date(int(end_d[0:4]),int(end_d[5:7]),int(end_d[8:10]))

    cursor = conn.execute("SELECT id, data  FROM Hours WHERE id='%s'" % last_id)
    for row in cursor:
        chwila = datetime.date(int(row[1][0:4]),int(row[1][5:7]),int(row[1][8:10]))
        minelo_start = (end_day - chwila).days + 1

    while end_d != now_h:
        cursor = conn.execute("SELECT id, data, temp_sr, temp_min, temp_max from Hours WHERE id>='%s'" % last_id)
        local_1 = datetime.date(int(row[1][0:4]),int(row[1][5:7]),int(row[1][8:10]))
        for row in cursor:
            local_2 = datetime.date(int(row[1][0:4]),int(row[1][5:7]),int(row[1][8:10]))
            warunek = (local_2 - local_1).days
            if warunek >= 1:
                last_id = row[0]
                break
            now_h = str(row[1])[0:10]

            min_avg = min_avg + float(row[3])
            max_avg = max_avg + float(row[4])
            avr_avg = avr_avg + float(row[2])
            avr_ind = avr_ind + 1

        cursor.execute('INSERT INTO Average VALUES(NULL, ?, ?, ?, ?);', ((local_1, round(avr_avg/avr_ind,2), round(min_avg/avr_ind,2), round(max_avg/avr_ind,2))))
        min_avg = NULL
        max_avg = NULL
        avr_avg = NULL
        avr_ind = NULL

        minelo = (end_day - local_2).days

        procent = round(100 - (minelo/minelo_start)*50,2)
        if kolej != local_2:
            print(str(procent) + "%")
            kolej = local_2

    print("Average Temp Calculation successfully")

def upload(way_1, way_2):
    try:
        way_2 = way_2.replace("Heat","Stats")
        shutil.copyfile(way_1, way_2)
        print("Done")
    except:
        print("\n\nCRASH sending\n\n")
        traceback.print_exc()
        raise SystemExit(0)

try:
    date1 = datetime.datetime.now()
    way_1 = "Stats.db"
    way_2 = "X:/Heat.db"
    way_3 = "Test/Heat.db"
    way_4 = "smb://RASPBERRYPI._smb._tcp.local/Python3/Heat.db"
    way_5 = "/Users/emsii/Downloads/Python/Stats.db"
    way_6 = "/Users/emsii/Downloads/Python/Heat.db"
    way_7 = "/Users/emsii/Downloads/Python/Stats2.db"
    #download(way_1, way_6)
    connect(way_1)
    tablica()
    calculating_temp()
    calculating_avg()

    cursor = conn.cursor()
    cursor.execute("DROP TABLE Temperatura")
    conn.commit()

    #upload(way_1,way_3)

    date2 = datetime.datetime.now()
    czas_minuty = int((date2 - date1).total_seconds()/60)
    czas_sekundy = int((date2 - date1).total_seconds()%60)
    print("Czas obliczen = " + str(czas_minuty) + ":" + str(czas_sekundy))

except ValueError:
    print("Crash")
    conn.commit()
    traceback.print_exc()
except ZeroDivisionError:
    print("Crash")
    conn.commit()
    traceback.print_exc()
except KeyboardInterrupt:
    conn.commit()
    print("STOP_KIboard")