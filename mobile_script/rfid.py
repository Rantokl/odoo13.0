import pyodbc
from datetime import date
import time
import threading

server = '10.68.222.61'
database = 'zk'
username = 'sa'
password = 'ZK+2023.'

countb =0

last_id = None
lock = threading.Lock()

connect_string= f"""DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=10.68.222.61,1433;DATABASE=ZKAccess;UID=sa;PWD=ZK+2023."""


        

conn = pyodbc.connect(connect_string)
cursor = conn.cursor()
    #print("connexion success!!")
try:
        
    #query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        #query = "SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'acc_monitor_log'"
    #query= "SELECT card_no, time, device_name FROM acc_monitor_log WHERE time = '2023-06-8'"
        query= "SELECT card_no, time, device_name, event_point_name FROM acc_monitor_log WHERE time between '2023-9-04 4:00:00' and '2023-9-04 23:00:00'"
    #query= "SELECT card_no, time, device_name FROM acc_monitor_log WHERE CAST(time AS DATE) = CAST(getdate() AS DATE) "
    #query2 = "SELECT id, card_no, time, device_name FROM acc_monitor_log WHERE  CAST(time AS DATE) = CAST(getdate() AS DATE), id > ? ORDER id ASC"
    #cursor.execute(query)
        cursor.execute(query)
    #tables = cursor.fetchall()
        rows = cursor.fetchall()
        #for row in rows:
        #    print(row)
        
        for row in rows:
            print(row)
           
            
            
            
        conn.close()
        
        
    
except pyodbc.Error as e:
    print(f'Erreur:{e}')
        
        
    

