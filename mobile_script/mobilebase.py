import pyodbc
from datetime import date
import time
import threading
import psycopg2
import datetime
from rpc import mailsend
server = 'localhost'
database = 'analytic_odoo'
username = 'postgres'
password = ''

countb =0
#card = 	'16134776'
#last_id = None

    #connect_string= f"""DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=10.68.222.61,1433;DATABASE=ZKAccess;UID=sa;PWD=ZK+2023."""
    #print(type(card))
connex = psycopg2.connect(database='analytic_odoo',
                          user = 'postgres',
                          password='1234',
                          host='localhost',
                          port='5432')


connex1 = psycopg2.connect(database='mobile_test',
                          user = 'postgres',
                          password='1234',
                          host='10.68.132.2',
                          port='5432')
try:
    curs1 = connex1.cursor()
    print("connected succesfully")
except Exception as e:
    print(e)
curs = connex.cursor()
query = """SELECT fv.id, fv.driver_id, vtr.name ,fv.license_plate
    FROM fleet_vehicle fv INNER JOIN fleet_vehicle_model vtr on vtr.id = fv.model_id 
    WHERE fv.tag_ids = '11';
    """
curs.execute(query)

rows = curs.fetchall()
vehicle_id = rows[0][0]
client_id = rows[0][1]
for row in rows:
    
    
    #print(row[0], model, plaque)
   
        
    curs1.execute("""INSERT INTO public."viseo_api_vehicle"(
	id,number,model,owner_id)
	VALUES (%s,%s,%s,%s)
 """,(row[0],row[3],row[2],row[1]))
        
    connex.commit()
    connex1.commit()
    count = curs1.rowcount
    print(count, "record created")

connex1.close()
connex.close()
 