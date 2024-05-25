import csv, sqlite3,datetime
first = datetime.date(2021,11,1)
dzis = datetime.date.today()
next = first
aktualny = first
connect = sqlite3.connect('Woda.db', check_same_thread=3)

while next != dzis:
    with open("MOSiR Jasło.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=';')
        for row in csvreader:
            try:
                global inwers
                inwers = datetime.date(int(row[0][6:10]),int(row[0][3:5]),int(row[0][0:2]))
  
            #print(inwers, next)
            
                if inwers == next:
                    print(inwers, next)
                    if row[3] != '':
                        #print(row[0], row[3])
                        if int(row[0][6:10]) == 2021:
                            #print(inwers)
                            if row[3] == "1":
                                zmiana = "9"
                            elif row[3] == "2":
                                zmiana = "10"
                            elif row[3] == "12":
                                zmiana = "11"
                            try:      
                                connect.execute('INSERT INTO GRAFIK VALUES(NULL, ?, ?)', (inwers, zmiana))
                            except sqlite3.IntegrityError:
                                pass 
                        elif int(row[0][6:10]) == 2022:
                            #print(inwers)
                            if row[3] == "1":
                                zmiana = "1"
                            elif row[3] == "2":
                                zmiana = "2"
                            elif row[3] == "12":
                                zmiana = "3"
                            try:      
                                connect.execute('INSERT INTO GRAFIK VALUES(NULL, ?, ?)', (inwers, zmiana))
                            except sqlite3.IntegrityError:
                                pass 
                        elif int(row[0][6:10]) == 2023:
                            #print(inwers)
                            if row[3] == "1":
                                zmiana = "12"
                            elif row[3] == "2":
                                zmiana = "13"
                            elif row[3] == "12":
                                zmiana = "14"
                            try:      
                                connect.execute('INSERT INTO GRAFIK VALUES(NULL, ?, ?)', (inwers, zmiana))
                            except sqlite3.IntegrityError:
                                pass                                     
            except ValueError:
                continue        
    next = next + datetime.timedelta(days=1)
    #print(first,dzis,next)                
connect.commit()
connect.close()