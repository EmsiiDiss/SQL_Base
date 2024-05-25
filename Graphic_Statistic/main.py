# Author: Emsii 
# Date: 20.05.2024
# https://github.com/EmsiiDiss


import sqlite3, datetime, os


def connect(file):
    connect = sqlite3.connect(file)
    print("Opened database successfully")
    return connect

def tablica(connect):
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
    connect.commit()



try:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    tablica(connect(database_file))


except:
    print("XDD")        