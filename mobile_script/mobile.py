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
connex = psycopg2.connect(database='viseo13_20230705_0830',
                          user = 'postgres',
                          password='',
                          host='10.68.163.4',
                          port='5432')


connex1 = psycopg2.connect(database='mobile_101023',
                          user = 'etech',
                          password='3Nyy22Bv',
                          host='10.68.132.2',
                          port='5432')
try:
    curs1 = connex1.cursor()
    print("connected succesfully")
except Exception as e:
    print(e)
curs = connex.cursor()
query = """SELECT DISTINCT rp.id, rp.name, rp.email ,rp.mobile
    FROM fleet_vehicle fv INNER JOIN res_partner rp on fv.driver_id = rp.id 
    WHERE fv.tag_ids = '11';
    """
curs.execute(query)

rows = curs.fetchall()
vehicle_id = rows[0][0]
client_id = rows[0][1]
for row in rows:
    
    
    #print(row[0], model, plaque)
   
        
    curs1.execute("""INSERT INTO public."viseoAccount_user"(
	id,name,email,mobile,is_active,date_joined,"isAdmin")
	VALUES (%s,%s,%s,%s,%s,%s,%s)
 """,(row[0],row[1],row[2],row[3],str(1),'2023-10-12 06:00:00+03',str(0)))
        
    connex.commit()
    connex1.commit()
    count = curs1.rowcount
    print(count, "record created")

connex1.close()
connex.close()
 