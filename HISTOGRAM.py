import datetime
import random
import statistics
import time
import pyodbc

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=AYUSHP-DELL\\SQLEXPRESS03;'
                            'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

def insert_data_histogram(cursor, values):
    table_name = 'Control_chart.dbo.[Histogram]'
    columns = ['SR_NO','DATETIME', 'BATCH', 'OC_POINTS']
    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?)"
    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database


