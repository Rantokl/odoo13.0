# -*- coding: utf-8 -*-
from custom_addons.viseo_mobile.models.database import dbconnex
from odoo import models, fields, api
import psycopg2

class Typedevis(models.Model):

    _inherit = 'fleet.claim.type'


    @api.model
    def create(self,vals):
        curs, connex = dbconnex(self)
        res = super(Typedevis, self).create(vals)
        curs.execute("""INSERT INTO public.viseo_api_typedevis(
        	id, name)
        	VALUES (%s, %s);
         """, (res.id, res.name))
        connex.commit()
        connex.close()

        return res


    def write(self,vals):
        curs, connex = dbconnex(self)

        res = super(Typedevis, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""UPDATE
                        public.viseo_api_typedevis
                        SET
                        id =%s, name =%s
                        WHERE id = %s;
                 """, (id, name,id))
        connex.commit()
        connex.close()
        return res


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
