# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api



class devis_sav(models.Model):
    _name = 'type.devis.sav'
#     _description = 'devis_sav.devis_sav'
    name = fields.Char('Type de devis')

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
    @api.model
    def create(self,vals):
        res = super(devis_sav, self).create(vals)
        connex = psycopg2.connect(database='mobile_sav',
                                  user='etech',
                                  password='3Nyy22Bv',
                                  host='10.68.132.2',
                                  port='5432')
        curs = connex.cursor()
        curs.execute("""INSERT INTO public."viseo_api_typedevis"(
        	id,name)
        	VALUES (%s,%s)
         """, (res.id, res.name))

        connex.commit()
        connex.close()

        return res

    def write(self, vals):
        connex = psycopg2.connect(database='mobile_sav',
                                  user='etech',
                                  password='3Nyy22Bv',
                                  host='10.68.132.2',
                                  port='5432')
        curs = connex.cursor()

        res = super(devis_sav, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""UPDATE
                        public.viseo_api_typedevis
                        SET
                        id =%s, name =%s
                        WHERE id = %s;
                 """, (id, name, id))
        connex.commit()
        connex.close()
        return res

