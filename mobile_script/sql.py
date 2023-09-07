import pyodbc
from datetime import date
import time
import threading
import psycopg2
import datetime
from rpc import mailsend
from vehicle import vehicle_info

from whats import sendsms
#from sms import sendsms
from rdv import rdvvehicle
import random

server = 'localhost'
database = 'odoo_rfid'
username = 'postgres'
password = ''

countb =0
card = 0
last_id = None
lock = threading.Lock()
connect_string= f"""DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=10.68.222.61,1433;DATABASE=ZKAccess;UID=sa;PWD=ZK+2023."""

connex = psycopg2.connect(database='odoo_rfid',
                          user = 'postgres',
                          password='1234',
                          host='localhost',
                          port='5432')

    
curs = connex.cursor()

while True:
    conn = pyodbc.connect(connect_string)
    cursor = conn.cursor()
    #print("connexion success!!")
    try:
        
    #query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    #query = "SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'acc_monitor_log'"
    #query= "SELECT card_no, time, device_name FROM acc_monitor_log WHERE time = '2023-06-8'"
    #query= "SELECT card_no, time, device_name FROM acc_monitor_log WHERE time between '2023-6-8 8:00:00' and '2023-6-8 23:00:00'"
    #query= "SELECT card_no, time, device_name FROM acc_monitor_log WHERE CAST(time AS DATE) = CAST(getdate() AS DATE) "
        query2 = "SELECT COUNT(*) FROM acc_monitor_log WHERE  CAST(time AS DATE) = CAST(getdate() AS DATE) "
    #cursor.execute(query)
        cursor.execute(query2)
    #tables = cursor.fetchall()
        count = cursor.fetchone()
        #for row in rows:
        #    print(row)
    
        count = count[0]
        if countb == count :
            time.sleep(1)
            
        else:
            countb = count
            print("data changed!!!")
            #print("number ", countb)
            query= "SELECT TOP 1 card_no, time, device_name, event_point_name FROM acc_monitor_log WHERE CAST(time AS DATE) = CAST(getdate() AS DATE) ORDER BY id DESC "
            cursor.execute(query)
            rows = cursor.fetchall()
            if card == rows[0][0]:
                print("Vehicle already passed!!! at : ", datetime.datetime.now(), "Location: ", rows[0][2] )
                time.sleep(1)
            else:   
                print("card id: ", rows[0][0])
                print("Time: ",rows[0][1])
                print("Location: ",rows[0][2])
                
                card = rows[0][0]
                tt = rows[0][1]
                loc = rows[0][2]
                if card == '' or card == '0':
            #query = "SELECT id FROM viseo_tag_rfid WHERE name = %s",(card,)
                #curs.execute("SELECT id FROM viseo_tag_rfid WHERE name = %s",(card,))
                    print("card without identifiant")
                else:
                    if loc == "Main":
                        vehicle_id, mdl, plq,eml, phone = vehicle_info(card)
                        
                        if mdl :
                #query = "SELECT name FROM fleet_vehicle WHERE tag_rfid = %s",((cc,))
                    #curs.execute("SELECT name FROM fleet_vehicle WHERE tag_rfid = %s",(cc,))
                    #vehicle = curs.fetchone()[0]
                    #print("Vehicle: ", mdl)
                            email, mobile, message = rdvvehicle(vehicle_id)
                            if message is None:
                                message = "Bonjour, bienvenue dans l'enceinte Viseo Andraharo."
                                sendsms(mobile,message)
                                #sendsms(mobile)
                                mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                            else:
                                sendsms(mobile,message)
                                #sendsms(mobile)
                                mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                                time.sleep(2)
                        else :
                            print("Vehicule: None, card not attributed!!!")
                            time.sleep(2)
            #print("id : ",cc)
                    else:
                        vehicle_id, mdl, plq,eml, phone = vehicle_info(card)
                        if mdl :
                #query = "SELECT name FROM fleet_vehicle WHERE tag_rfid = %s",((cc,))
                    #curs.execute("SELECT name FROM fleet_vehicle WHERE tag_rfid = %s",(cc,))
                    #vehicle = curs.fetchone()[0]
                    #print("Vehicle: ", mdl)
                            #sms= "Bonjour, veuillez prendre votre parking habituel."
                            email, mobile, message = rdvvehicle(vehicle_id)
                            if message is None:
                                message = "Bonjour, bienvenue dans l'enceinte Viseo Andraharo."
                                sendsms(mobile,message)
                                #sendsms(mobile)
                            else:
                                sendsms(mobile,message)
                                #sendsms(mobile)
                                mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                                time.sleep(2)
                            #sendsms(mobile,sms)
                            #mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                            #time.sleep(2)
                        else :
                            print("Vehicule: None, card not attributed!!!")
                            time.sleep(2)
                        
            
        conn.close()
        
        
    
    except pyodbc.Error as e:
        print(f'Erreur:{e}')
        
        
    

