from time import strftime
import psycopg2
from odoo import models, fields, api

class Reclamationsav(models.Mode):
    _inherit='fleet.claim'
    reclam_id = fields.Integer()

    def reclamation(self):
        conn = psycopg2.connect(database='mobile_sav',
                          user = 'etech',
                          password='3Nyy22Bv',
                          host='10.68.132.2',
                          port='5432')

        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.viseo_api_reclamation;")
        rows = cur.fetchall()
        
        if rows:
            for row in rows:
                existing_record= self.env['fleet.claim'].search([('reclam_id','=',row[0])])
                if existing_record:
                    continue
                
                record = {
                    'rdv_id' : row[0],
                    'user_id':row[2],
                    'note':row[1],
                    'vehicle_id':row[5],
                    'staten':row[4],
                    'date_rdv':strftime(str(row[7])),
                    'status':'draft'
                }
                
                self.env['viseo_rdv_mobile.viseo_rdv_mobile'].create(record)