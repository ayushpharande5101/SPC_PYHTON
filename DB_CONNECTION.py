import pyodbc

# Replace 'your_username' and 'your_password' with your actual username and password
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                           'Server=spc-12.database.windows.net;'
                           'UID=Ayush;'
                           'PWD=Rajashri@123;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()


