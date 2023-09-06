from odoo import models, fields, api


class Typerdv(models.Model):
    _name= 'type_rdv.type_rdv'


    # atelier = fields.Selection(related='at.atelier')
    name = fields.Char("Type de rendez-vous")