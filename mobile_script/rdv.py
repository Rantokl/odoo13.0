import pyodbc
from datetime import date
import time
import threading
import psycopg2
import datetime
from rpc import mailsend
server = 'localhost'
database = 'odoo_rfid'
username = 'postgres'
password = ''
import random
countb =0
#card = 	'16134776'
#last_id = None


def rdvvehicle(id_vehicle):
    #connect_string= f"""DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=10.68.222.61,1433;DATABASE=ZKAccess;UID=sa;PWD=ZK+2023."""
    #print(type(card))
    connex = psycopg2.connect(database='analytic_odoo',
                          user = 'postgres',
                          password='1234',
                          host='localhost',
                          port='5432')


    
    curs = connex.cursor()
    query = """SELECT vehicle_id from viseo_rdv_mobile_viseo_rdv_mobile WHERE  vehicle_id = %s and status = 'accepted' and CAST(date_rdv as DATE) = CAST(%s AS DATE)
    
    """
    
    
    
    curs.execute(query,(id_vehicle,datetime.date.today(),))

    """SELECT fv.name, fv.driver_id, vtr.name 
    FROM fleet_vehicle fv INNER JOIN fleet_vehicle_model vtr on vtr.id = fv.model_id 
    WHERE fv.id = 5346;
    """
    """SELECT fv.id, fv.driver_id, vtr.name 
                FROM fleet_vehicle fv INNER JOIN viseo_tag_rfid vtr on vtr.id = fv.tag_rfid 
                WHERE vtr.name = %s 
            """

    vehicles = curs.fetchall()
    print(vehicles)
    if not vehicles:
        print("Pas de rdv")
        email = "alt.dev@viseo.mg"
        mobile = "+261344901849"
        message = "Bonjour, bienvenue à Ocean Trade, nous vous souhaitons une excellente journée"
        return email, mobile, message
    else:
        vehicle_id = vehicles[0][0]
        #print("vehicle id:", vehicle_id)
        #email_id = vehicles[0][1]
        query = """SELECT fv.id, fv.driver_id, vtr.name 
                FROM fleet_vehicle fv INNER JOIN viseo_tag_rfid vtr on vtr.id = fv.tag_rfid 
                WHERE fv.id = %s 
            """
        curs.execute(query,(vehicle_id,))
    
        vehicle = curs.fetchall()
    
        if vehicle:
            email_id = vehicle[0][1]
            curs.execute("""SELECT vtr.name, fv.license_plate
                        FROM fleet_vehicle fv INNER JOIN fleet_vehicle_model vtr on vtr.id = fv.model_id 
                        WHERE CAST(fv.id AS INTEGER) = CAST(%s AS INTEGER);
                        """,(vehicle_id,))


            models = curs.fetchall()

            model = models[0][0]
            plaque = models[0][1]
    
            curs.execute("SELECT email, phone, customer_classement FROM res_partner WHERE id = %s",(email_id,))
            emails = curs.fetchall()
            email = emails[0][0]
            mobile = emails[0][1]
            print("Vehicle : ", model)
            print("Plaque d'imatriculation: ", plaque)
            print("Email : ", email)
            print("Téléphone : ", mobile)
            #sms = "Bienvenue à Ocean Trade, nous vous remercions pour votre rendez-vous, veuillez prendre le parking N° "+str(random.randint(1,15))
            sms = emails[0][2]
            return email, mobile, sms
        else:
            print("Card not attributee")
            vehicle_id = None
            model = None
            plaque = None
            email = None
            mobile = None
            return email, mobile
     
   

