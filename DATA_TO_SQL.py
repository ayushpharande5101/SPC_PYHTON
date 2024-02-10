import random
import statistics
import time
import pyodbc

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                           'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                           'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

def insert_data(cursor, values):
    table_name = 'Control_chart.dbo.[SPC_SAMPLE_DATA1]'

    columns = ['SR_NO', '[1]', '[2]', '[3]', '[4]', '[5]','X_MAX','X_MIN','AVERAGE','RANGE']

    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

DATA = []

j = 1
while True:
    Dosing_Weight = random.randint(400,500)

    DATA.append(Dosing_Weight)

    if len(DATA) <= 2:
        STD = 0
    else:
        STD = statistics.stdev(DATA)
    print(STD)
    if len(DATA) >= 5:

        print(f"DATA: ",DATA)
        AVERAGE = statistics.mean(DATA)
        X_MAX = max(DATA)
        print(f"MAXIMUM:",X_MAX)
        X_MIN = min(DATA)
        print(f"MINIMUM:",X_MIN)
        RANGE = max(DATA) - min(DATA)
        values = (j/5, DATA[0], DATA[1], DATA[2], DATA[3],DATA[4],X_MAX, X_MIN, AVERAGE,RANGE)
        print(values)
        time.sleep(2)
        insert_data(cursor, values)
        DATA.clear()
        print("DATA INSERTED")
        time.sleep(1)
    j = j + 1



