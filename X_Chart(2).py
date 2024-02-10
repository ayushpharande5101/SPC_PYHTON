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
    table_name = 'Control_chart.dbo.[SPC_SAMPLE_DATA]'

    columns = ['SR_NO', '[1]', '[2]', '[3]', '[4]', '[5]','X_MAX','X_MIN','AVERAGE','RANGE','OVERALL_AVERAGE','OVERALL_RANGE','UCL_X','LCL_X']

    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

DATA = []
AVG = []
RNG = []

j = 1
while True:
    Dosing_Weight = random.randint(400,500)

    time.sleep(2)

    DATA.append(Dosing_Weight)

    if len(DATA) <= 2:
        STD = 0
    else:
        STD = statistics.stdev(DATA)
    print(STD)

    if len(DATA) >= 5:
        print(f"DATA: ",DATA)
        AVERAGE = statistics.mean(DATA)
        AVG.append(AVERAGE)

        X_MAX = max(DATA)
        print(f"MAXIMUM:",X_MAX)

        X_MIN = min(DATA)
        print(f"MINIMUM:",X_MIN)

        RANGE = max(DATA) - min(DATA)
        RNG.append(RANGE)

        if len(AVG) >= 2:
            OVERALL_AVERAGE = statistics.mean(AVG)
        else:
            OVERALL_AVERAGE = 0

        if len(RNG) >= 2:
            OVERALL_RANGE = statistics.mean(RNG)
        else:
            OVERALL_RANGE = 0

        if OVERALL_AVERAGE == 0 and OVERALL_RANGE == 0:
            UCL_X_CHART = 0
            LCL_X_CHART = 0
        else:
            UCL_X_CHART = OVERALL_AVERAGE + (0.577 * OVERALL_RANGE)
            LCL_X_CHART = OVERALL_AVERAGE - (0.577 * OVERALL_RANGE)

        values = (j/5, DATA[0], DATA[1], DATA[2], DATA[3], DATA[4], X_MAX, X_MIN, AVERAGE,RANGE,OVERALL_AVERAGE,OVERALL_RANGE,UCL_X_CHART, LCL_X_CHART)
        print(values)
        time.sleep(2)
        insert_data(cursor, values)
        DATA.clear()
        print("DATA INSERTED")
        time.sleep(1)

    else:
        print("Updating Values")
    j = j + 1



