# Author: Emsii
# Date: 05.08.204
# https://github.com/EmsiiDiss

import sqlite3, shutil, datetime, traceback, os
import numpy as np
import pandas as pd

# from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.dates as dates

class Datas:
    def __init__(self, date=None, time=None, temp=None, temp_avr=None, temp_min=None, temp_max=None) -> None:
        self.date = date
        self.time = time
        self.temp = temp
        self.temp_avr = temp_avr
        self.temp_min = temp_min
        self.temp_max = temp_max

class dictionery:
    def date_and_time(base):
        temperatures_by_date_hour = {}
        for _, row in base.iterrows():
            date = row['date']
            time = row['time']
            temperature = row['temperature']

            key = (date, time)

            if key not in temperatures_by_date_hour:
                temperatures_by_date_hour[key] = []
            temperatures_by_date_hour[key].append(temperature)
        return temperatures_by_date_hour

    def date(base, target):
        temperatures_by_date_hour = {}
        for _, row in base.iterrows():
            date = row['date']
            temperature = row[target]

            key = (date)

            if key not in temperatures_by_date_hour:
                temperatures_by_date_hour[key] = []
            temperatures_by_date_hour[key].append(temperature)
        return temperatures_by_date_hour

    def search_averge_v2(base):
        temperatures_by_date_hour = {}
        for _, row in base.iterrows():
            date = row['DATA']
            temp_sr = row['TEMP_AVERAGE']
            temp_min = row['TEMP_MIN']
            temp_max = row['TEMP_MAX']

            key = (date)

            if key not in temperatures_by_date_hour:
                temperatures_by_date_hour[key] = []
            temperatures_by_date_hour[key].append([temp_sr, temp_min, temp_max])
        return temperatures_by_date_hour        


    def search_averge(base):
        temp_sr_by_date = {}
        temp_min_by_date = {}
        temp_max_by_date = {}

        for _, row in base.iterrows():
            date = row['date']
            temp_sr = row['temp_sr']
            temp_min = row['temp_min']
            temp_max = row['temp_max']

            key = (date)

            if key not in temp_sr_by_date:
                temp_sr_by_date[key] = []
                temp_min_by_date[key] = []
                temp_max_by_date[key] = []
                
            temp_sr_by_date[key].append(temp_sr)
            temp_min_by_date[key].append(temp_min)
            temp_max_by_date[key].append(temp_max)

        return temp_sr_by_date, temp_min_by_date, temp_max_by_date   
    

class calc:
    def date_and_time(temperatures_by_date_hour):
        data = []
        for key, temps in temperatures_by_date_hour.items():
            date, hour = key
            avg_temp = round(np.mean(temps),2)
            min_temp = np.min(temps)
            max_temp = np.max(temps)
            data.append((date, hour + ":00:00", avg_temp, min_temp, max_temp))
        data_array = np.array(data, dtype=[('date', 'U10'), ('hour + ":00:00"', 'U10'), ('avg_temp', 'U5'), ('min_temp', 'U5'), ('max_temp', 'U5')])
        return data_array
        
    def date(temperatures_by_date_hour):
        data = []
        for key, temps in temperatures_by_date_hour.items():
            date = key
            avg_temp = round(np.mean(temps), 2)
            min_temp = np.min(temps)
            max_temp = np.max(temps)
            data.append((date, avg_temp, min_temp, max_temp))
        data_array = np.array(data, dtype=[('date', 'U10'), ('avg_temp', 'U5'), ('min_temp', 'U5'), ('max_temp', 'U5')])
        return data_array       

##\/ This is process 
    def averge_all(temperatures_by_date_hour):
        data = []
        for key, temps in temperatures_by_date_hour.items():
            date = key
            avg_temp = round(np.mean(temps), 2)
            data.append((date, avg_temp))
        data_array = np.array(data, dtype=[('date', 'U10'), ('Average', 'U10')])
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
                TIME varchar(250) NOT NULL,
                TEMP_AVERAGE varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")

        connect.execute("""
            CREATE TABLE IF NOT EXISTS Days (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_AVERAGE varchar(250) NOT NULL,
                TEMP_MIN varchar(250) NOT NULL,
                TEMP_MAX varchar(250) NOT NULL
            )""")
        
        connect.execute("""
            CREATE TABLE IF NOT EXISTS Average (
                id INTEGER PRIMARY KEY ASC,
                DATA varchar(250) NOT NULL,
                TEMP_day_AVERAGE varchar(250) NOT NULL,
                TEMP_day_MIN varchar(250) NOT NULL,
                TEMP_day_MAX varchar(250) NOT NULL
            )""")
        
    def connect(place):
        return sqlite3.connect(place)

    def take_full(file):
        connect = SQLbase.connect(file)
        cursor = connect.cursor()
        cursor.execute("SELECT data, godzina, temp_dot FROM Temperatura")
        data = cursor.fetchall()
        column_name = np.array(data, dtype=[('date', 'U10'), ('time', 'U2'), ('temperature', 'float64')])
        base = pd.DataFrame(column_name, columns=['date', 'time', 'temperature'])
        return base

    def take_Hours(file, table):
        connect = SQLbase.connect(file)
        cursor = connect.cursor()
        string = "SELECT * FROM " + table
        cursor.execute(string)
        data = cursor.fetchall()
        column_name = np.array(data, dtype=[("id", "U10"), ('date', 'U10'), ('time', 'U2'), ('temp_average', 'float64'), ('temp_min', 'float64'), ('temp_max', 'float64')])
        base = pd.DataFrame(column_name, columns=['id', 'date', 'time', 'temp_average', 'temp_min', 'temp_max'])
        return base

    def insert(place, data, where, columns ):
        connect = SQLbase.connect(place)
        question_marks = columns * ",?"
        table = str("INSERT INTO " + where + " VALUES(NULL" + question_marks + ");")
        connect.executemany(table, data)
        connect.commit()
        connect.close()

    def update(place,):
        connect = SQLbase.connect(place)

try:
    Heat = "C:\GitHUB\SQL_Base\Temp_Room_Statistic\Heat.db"
    Stats2 = "C:\GitHUB\SQL_Base\Temp_Room_Statistic\Stats2.db"

    SQLbase.create(Stats2)

    date1 = datetime.datetime.now()
    
    data = SQLbase.take_full(Heat)
    Heat = Datas(date=data['date'], time=data['time'], temp=data['temperature']) #test
    date_and_time = dictionery.date_and_time(data)
    date_time = calc.date_and_time(date_and_time)
    SQLbase.insert(Stats2, date_time, "Hours", 5)

    date = dictionery.date(data, "temperature")
    date_data = calc.date(date)
    SQLbase.insert(Stats2, date_data, "Days", 4)
    date2 = datetime.datetime.now()
    
    avrg = SQLbase.take_Hours(Stats2, "Hours")
    avrg_averge =   dictionery.date(avrg, 'temp_average')
    avrg_min    =   dictionery.date(avrg, 'temp_min')
    avrg_max    =   dictionery.date(avrg, 'temp_max')

    avrg_averge = calc.averge_all(avrg_averge)
    avrg_min = calc.averge_all(avrg_min)
    avrg_max = calc.averge_all(avrg_max)

    avrg_averge = dict(avrg_averge)
    avrg_min = dict(avrg_min)
    avrg_max = dict(avrg_max)

    average_day = pd.DataFrame({'TEMP_day_AVERAGE':avrg_averge, 'TEMP_day_MIN':avrg_min, "TEMP_day_MAX":avrg_max})

    average_day.reset_index(inplace=True)
    average_day.rename(columns={'index': 'Date'}, inplace=True)
    data_to_insert = average_day.values.tolist()
    SQLbase.insert(Stats2, data_to_insert, "Average", 4)

    # print(average_day)

    # print(avrg_averge)    
    print(int((date2 - date1).seconds))
    
except KeyboardInterrupt:
    print("UPS!")    