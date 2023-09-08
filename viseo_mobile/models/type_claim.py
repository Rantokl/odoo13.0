# -*- coding: utf-8 -*-
from . import database
from odoo import models, fields, api
import psycopg2

class TypeReclamation(models.Model):

    _inherit = 'fleet.claim.type'


    @api.model
    def create(self,vals):
        curs, connex = database.dbconnex(self)
        res = super(TypeReclamation, self).create(vals)
        curs.execute("""INSERT INTO public.viseo_api_typereclamation(
        	id, name)
        	VALUES (%s, %s);
         """, (res.id, res.name))
        connex.commit()
        connex.close()

        return res


    def write(self,vals):
        curs, connex = database.dbconnex(self)

        res = super(TypeReclamation, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""UPDATE
                        public.viseo_api_typereclamation
                        SET
                        id =%s, name =%s
                        WHERE id = %s;
                 """, (id, name,id))
        connex.commit()
        connex.close()
        return res

    def unlink(self):
        res = super(TypeReclamation,self).unlink()
        id = self.id
        print(id)
        curs, connex = database.dbconnex(self)
        curs.execute("""DELETE FROM public.viseo_api_typereclamation 
        WHERE id = %s
        """, (str(id)))
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
