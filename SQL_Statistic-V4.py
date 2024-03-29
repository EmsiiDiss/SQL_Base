# Author: Emsii
# Date: 26.10.2022
# https://github.com/EmsiiDiss

import sqlite3, shutil, datetime, traceback
from tabulate import tabulate

from tkinter import *

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as dates

def upload(way_1, way_2):
    shutil.copyfile(way_1, way_2)
    print("Done")

def connect(way_1, way_2):
    try:
        global conn, connect
        conn = sqlite3.connect(way_1)
        connect = sqlite3.connect(way_2)
        print("Opened database successfully")

    except:
        print("\n\nCRASH Opened database\n\n")
        traceback.print_exc()
        raise SystemExit(0)

def tablica():
    try:
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
        connect.execute("""
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

def insert_to_tab(chwila, avr, min_list, max_list, where):
    space = str("INSERT INTO " + where + " VALUES(NULL, ?, ?, ?, ?);")
    if where == "Average":
        connect.execute(space, (chwila, averageXD(avr), averageXD(min_list), averageXD(max_list)))
    else:
        connect.execute(space, (chwila, averageXD(avr), min(min_list), max(max_list)))

def reset_avr_list():
    global list_avr_avr, list_avr_min, list_avr_max

    list_avr_min = []
    list_avr_max = []
    list_avr_avr = []

def calc_temp_avr(list):
    global list_avr_min, list_avr_max, list_avr_avr

    list_avr_min.append(min(list))
    list_avr_max.append(max(list))
    list_avr_avr.append(averageXD(list))

list_hours = []
def calc_temp_hours(data, godzina, temp, index, last_index):
    global chwila_hours, list_hours

    here = datetime.datetime(int(data[0:4]), int(data[5:7]), int(data[8:10]), int(godzina[0:2]))
    if chwila_hours != here:
        insert_to_tab(chwila_hours, list_hours, list_hours, list_hours, "Hours")
        calc_temp_avr(list_hours)
        chwila_hours = here
        list_hours = []
        list_hours.append(float(temp))

    elif index == last_index:
        list_hours.append(float(temp))
        insert_to_tab(chwila_hours, list_hours, list_hours, list_hours, "Hours")
        calc_temp_avr(list_hours)

    else:
        list_hours.append(float(temp))

list_days = []
def calc_temp_days(data, temp, index, last_index):
    global chwila_days, list_days

    here = datetime.date(int(data[0:4]), int(data[5:7]), int(data[8:10]))
    if chwila_days != here:
        insert_to_tab(chwila_days, list_days, list_days, list_days, "Days")
        insert_to_tab(chwila_days, list_avr_avr, list_avr_min, list_avr_max, "Average")
        reset_avr_list()
        chwila_days = here
        list_days = []
        list_days.append(float(temp))

    elif index == last_index:
        list_days.append(float(temp))
        insert_to_tab(chwila_days, list_days, list_days, list_days, "Days")
        insert_to_tab(chwila_days, list_avr_avr, list_avr_min, list_avr_max, "Average")
        reset_avr_list()

    else:
        list_days.append(float(temp))

def averageXD(list):
    return round(sum(list) / len(list), 2)

def calculator(data_start, data_end):
    global chwila_hours, list_hours, chwila_days, list_days
    print(data_start,data_end)
    list_hours = []
    list_days = []

    print("Starting calculation")
    if data_end == "0" or data_end == 0:
        cursor = conn.execute("SELECT id FROM Temperatura ORDER BY id DESC LIMIT 1")
        for row in cursor:
            last_index = row[0]
    else:
        cursor = conn.execute("SELECT id FROM Temperatura WHERE data=?", data_start)
        for row in cursor:
            last_index = row[0]

    if data_start == "0" or data_end == 0:
        cursor = conn.execute("SELECT id, godzina, data FROM temperatura WHERE id=1")
        for row in cursor:
            chwila_hours = datetime.datetime(int(row[2][0:4]), int(row[2][5:7]), int(row[2][8:10]), int(row[1][0:2]))
            chwila_days = datetime.date(int(row[2][0:4]), int(row[2][5:7]), int(row[2][8:10]))
    else:
        cursor = conn.execute("SELECT id, godzina, data FROM temperatura WHERE data=?", data_start)
        for row in cursor:
            chwila_hours = datetime.datetime(int(row[2][0:4]), int(row[2][5:7]), int(row[2][8:10]), int(row[1][0:2]))
            chwila_days = datetime.date(int(row[2][0:4]), int(row[2][5:7]), int(row[2][8:10]))


    cursor = conn.execute("SELECT id, godzina, data, temp_dot FROM temperatura")
    for row in cursor:
        calc_temp_hours(row[2],row[1],row[3], row[0], last_index)
        calc_temp_days(row[2], row[3], row[0], last_index)

x = []
y1 = []
y2 = []
y3 = []

def linreg():
    global x, y1, y2, y3
    cursor = connect.execute("SELECT data, Temp_sr, Temp_min, temp_max id FROM Days")
    for row in cursor:
        x.append(row[0])
        y1.append(float(row[1]))
        y2.append(float(row[2]))
        y3.append(float(row[3]))
def plot_trend(x_num, xd):
    return np.polyfit(x_num, xd, 1)

def example_plot(ax, time, value, what):
    if what == "Average":
        ax.xaxis.tick_top()
    ax.plot(time, value, label = what)
    ax.grid(True)
    ax.set_xlabel('Data', fontsize=8)
    ax.set_ylabel('Temp [*C]', fontsize=8)
    ax.set_title(what, fontsize=8)
    ax.tick_params(axis='x', labelrotation = 45)

    x_num = dates.date2num(time)
    fit = np.poly1d(plot_trend(x_num, value))
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot(x_fit, fit(x_fit), label = what + " Trend")
    ax.legend()

def trend_example_plot(ax, time, value, what):
    x_num = dates.date2num(time)
    fit = np.poly1d(plot_trend(x_num, value))
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot(dates.num2date(x_fit), fit(x_fit), label=what+" Trend")
    ax.legend()

    ax.grid(True)
    ax.set_xlabel('Data', fontsize=8)
    ax.set_ylabel('Temp [*C]', fontsize=8)
    ax.tick_params(axis='x', labelrotation = 45)

def plotPrint():
    linreg()

    times = pd.DatetimeIndex(data=x)
    df = pd.DataFrame({'Time': times,
                       'Average': y1,
                       'Minimal': y2,
                       'Maximal': y3})

    fig = plt.figure()
    fig.set_figheight(6)
    fig.set_figwidth(12)
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=4, rowspan=2)
    ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
    example_plot(ax = ax1, time = df['Time'], value= df['Average'], what="Average")
    example_plot(ax = ax3, time = df['Time'], value= df['Minimal'], what="Minimal")
    example_plot(ax = ax4, time = df['Time'], value= df['Maximal'], what="Maximal")

    fig = plt.figure()
    ax0 = plt.subplot2grid((1, 1),(0, 0))
    trend_example_plot(ax = ax0, time = df['Time'], value = df['Average'], what="Average")
    trend_example_plot(ax = ax0, time = df['Time'], value = df['Minimal'], what="Minimal")
    trend_example_plot(ax = ax0, time = df['Time'], value = df['Maximal'], what="Maximal")
    plt.show()

try:
    if input("0. If printing all ender 0\n1. Ender 1 to calculation okresion \n") == (0 or "0"):
        data_start = 0
        data_end = 0
    else:
        data_start = input("Enter start date: YYYY-MM-DD\n")
        data_end = input("Enter end date: YYYY-MM-DD\n")
    date1 = datetime.datetime.now()
    way_1 = "Stats.db"
    way_15 = "Heat.db"
    way_2 = "X:/Heat.db"
    way_25 = "X:/Stats.db"
    way_3 = "Test/Heat.db"
    way_4 = "r'//RASPBERRYPI._smb._tcp.local/Python3/Heat.db"
    way_41 = "r'//RASPBERRYPI._smb._tcp.local/Python3/Stats.db"
    way_5 = "/Users/emsii/Downloads/Python/Stats.db"
    way_6 = "/Users/emsii/Downloads/Python/Heat.db"
    way_7 = "/Users/emsii/Downloads/Python/Stats2.db"

    try:
        upload(way_2,way_15)
    except:
        print("\nDownlaod failed!\n")

    connect(way_15, way_1)
    tablica()
    reset_avr_list()
    calculator(data_start, data_end)

    conn.commit()
    connect.commit()

    try:
        upload(way_1,way_25)
    except:
        print("\nUpload failed!\n")

    date2 = datetime.datetime.now()
    time_calc = int((date2 - date1).microseconds)
    time_us = int(time_calc%1000)
    time_ms = int(time_calc/1000%1000)
    time_sek = int(time_calc/1000000%60)
    time_min = int(time_calc/60000000)
    timer = [['', 'Minutes', 'Seconds', 'Millisecond', 'Microsecend'], ["Calculation time", time_min, time_sek, time_ms, time_us]]
    print(tabulate(timer, headers='firstrow', tablefmt='fancy_grid'))
    plotPrint()

except ValueError:
    print("Crash")
    conn.commit()
    traceback.print_exc()

except KeyboardInterrupt:
    conn.commit()
    print("STOP_KIboard")