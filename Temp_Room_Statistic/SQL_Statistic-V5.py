# Author: Emsii
# Date: 05.08.204
# https://github.com/EmsiiDiss

import sqlite3, shutil, datetime, traceback, os
import numpy as np
import pandas as pd

# from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.dates as dates


class calc:
    def search(base):
        data = []
        temperatures_by_date_hour = {}
        for _, row in base.iterrows():
            date = row['date']
            time = row['time']
            temperature = row['temperature']

            key = (date, time)

            if key not in temperatures_by_date_hour:
                temperatures_by_date_hour[key] = []
            temperatures_by_date_hour[key].append(temperature)

        for key, temps in temperatures_by_date_hour.items():
            date, hour = key
            avg_temp = round(np.mean(temps),2)
            min_temp = np.min(temps)
            max_temp = np.max(temps)
            date_hours_str = date + " " + hour + ":00:00"
            data.append((date_hours_str, avg_temp, min_temp, max_temp))
        data_array = np.array(data, dtype=[('date_hours_str', 'U19'), ('avg_temp', 'U10'), ('min_temp', 'U10'), ('max_temp', 'U10')])
        return data_array
        

class SQLbase:
    def create(place):
        connect = SQLbase.connect(place)

        cursor = connect.cursor()
        cursor.execute("DROP TABLE IF EXISTS Hours")
        cursor.execute("DROP TABLE IF EXISTS Days")
        cursor.execute("DROP TABLE IF EXISTS Average")
        connect.execute("""
            CREATE TABLE IF NOT EXISTS Hours (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")

        connect.execute("""
            CREATE TABLE IF NOT EXISTS Days (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_SR varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")

    def connect(place):
        return sqlite3.connect(place)

    def take(place):
        connect = SQLbase.connect(place)
        cursor = connect.cursor()
        cursor.execute("SELECT data, SUBSTR(godzina, 1, 2), temp_dot FROM Temperatura")
        data = cursor.fetchall()
        A = np.array(data, dtype=[('date', 'U10'), ('time', 'U8'), ('temperature', 'float64')])
        B = pd.DataFrame(A, columns=['date', 'time', 'temperature'])
        return B

    def insert(place, data, where):
        connect = SQLbase.connect(place)
        table = str("INSERT INTO " + where + " VALUES(NULL, ?, ?, ?, ?);")
        connect.executemany(table, data)
        connect.commit()

try:
    Heat = "C:\GitHUB\SQL_Base\Temp_Room_Statistic\Heat.db"
    Stats2 = "C:\GitHUB\SQL_Base\Temp_Room_Statistic\Stats2.db"
    SQLbase.create(Stats2)
    data = calc.search(SQLbase.take(Heat))
    SQLbase.insert(Stats2, data, "Hours")

except KeyboardInterrupt:
    print("UPS!")    