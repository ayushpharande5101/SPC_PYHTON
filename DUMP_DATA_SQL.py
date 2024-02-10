import datetime
import random
import statistics
import time
import statistics
import pyodbc
import pandas as pd

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                           'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                           'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

def insert_data_Xchart(cursor, values):
    table_name = 'Control_chart.dbo.[X_CHART]'

    columns = ['SR_NO', 'DATETIME', 'BATCH_NO', 'PART_ID', 'DOSING_WEIGHT', 'AVERAGE','RANGE','UCL_X','LCL_X','USL_X','LSL_X','cpK_X','cp_X']

    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)"

    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

DATETIME = datetime.datetime.now()
values = (0,DATETIME,0,0,0,0,0,0,0,0,0,0,0)
insert_data_Xchart(cursor,values)

