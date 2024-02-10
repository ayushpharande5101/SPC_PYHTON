import datetime
import random
import statistics
import time
import pyodbc
import pandas as pd

# Define the connection string
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=AYUSHP-DELL\\SQLEXPRESS03;'
                            'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

def insert_data(cursor, values):
    table_name = 'Control_chart.dbo.[SPC_SAMPLE_DATA]'
    columns = ['SR_NO','[1]', '[2]', '[3]', '[4]', '[5]']
    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

def insert_data_Xchart(cursor, values):
    table_name = 'Control_chart.dbo.[X_CHART]'
    columns = ['SR_NO','DATETIME', 'BATCH_NO', 'PART_ID', 'DOSING_WEIGHT', 'AVERAGE', 'RANGE', 'UCL_X', 'LCL_X', 'USL_X', 'LSL_X', 'cpK_X', 'cp_X','OVERALL_AVERAGE','OVERALL_RANGE']
    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

j = 1
r = 0
DATA = []
Average = []
Range = []

while True:
    Dosing_Weight = random.randint(400,500)
    A25 = Dosing_Weight

    DATA.append(Dosing_Weight)

    if len(DATA) <= 2:
        STD = 0
    else:
        STD = statistics.stdev(DATA)
    print(STD)

    if len(DATA) >= 5:
        K = j/5 + 1
        if K == 0:
            break
        else:
            values = (K, DATA[0], DATA[1], DATA[2], DATA[3], DATA[4])
            insert_data(cursor, values)
        DATA.clear()
        print("DATA INSERTED")
        time.sleep(1)

    try:
        sql_query = 'SELECT * FROM [Control_chart].[dbo].[SPC_SAMPLE_DATA]'
        df = pd.read_sql(sql_query, connection)
        A1 = df.iloc[:, 1:].values.flatten()

        MEAN = statistics.mean(A1)
        MAX = max(A1)
        MIN = min(A1)
        RANGE = MAX - MIN
        Average.append(MEAN)
        Range.append(RANGE)

        OVERALL_RANGE = statistics.mean(Range)
        OVERALL_AVERAGE = statistics.mean(Average)

        UCL_X_CHART = OVERALL_AVERAGE + (0.577 * OVERALL_RANGE)
        LCL_X_CHART = OVERALL_AVERAGE - (0.577 * OVERALL_RANGE)

        print(f"AVERAGE: {Average}")
        print(f"RANGE: {Range}")
        print(f"OVERALL_RANGE: {OVERALL_RANGE}")
        print(f"OVERALL_AVERAGE: {OVERALL_AVERAGE}")
        print(f"UCL_X_CHART: {UCL_X_CHART}")
        print(f"LCL_X_CHART: {LCL_X_CHART}")

        DATETIME = datetime.datetime.now()
        K = j
        # if K == 0:
        #     continue
        # else:
        values = (K, DATETIME, 1, 'A123', A1[0+r], MEAN, RANGE, UCL_X_CHART, LCL_X_CHART, 0, 0, 0, 0,OVERALL_AVERAGE,OVERALL_RANGE)
        insert_data_Xchart(cursor, values)
        print("DATA INSERTED SUCCESSFULLY")
        time.sleep(3)

        j = j + 1
        r = r + 1

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(2)




