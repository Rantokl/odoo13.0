# -*- coding: utf-8 -*-
from . import database
from odoo import models, fields, api
import psycopg2

class TypeRdv(models.Model):

    _inherit = 'type_rdv.type_rdv'


    @api.model
    def create(self,vals):
        curs, connex = database.dbconnex(self)
        res = super(TypeRdv, self).create(vals)
        curs.execute("""INSERT INTO public.viseo_api_typerendezvous(
        	id, name)
        	VALUES (%s, %s);
         """, (res.id, res.name))
        connex.commit()
        connex.close()

        return res


    def write(self,vals):
        curs, connex = database.dbconnex(self)

        res = super(TypeRdv, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""UPDATE
                        public.viseo_api_typerendezvous
                        SET
                        id =%s, name =%s
                        WHERE id = %s;
                 """, (id, name,id))
        connex.commit()
        connex.close()
        return res
    
    def write(self,vals):
        curs, connex = database.dbconnex(self)

        res = super(TypeRdv, self).write(vals)
        id = self.id
        name = self.name
        curs.execute("""UPDATE
                        public.viseo_api_typerendezvous
                        SET
                        id =%s, name =%s
                        WHERE id = %s;
                 """, (id, name,id))
        connex.commit()
        connex.close()
        return res

    def unlink(self):
        res = super(TypeRdv,self).unlink()
        id = self.id
        print(id)
        curs, connex = database.dbconnex(self)
        curs.execute("""DELETE FROM public.viseo_api_typerendezvous 
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
