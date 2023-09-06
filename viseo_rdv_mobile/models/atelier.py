from odoo import models, fields, api

class pont_vehicle(models.Model):
    _name = 'pont_vehicle.pont_vehicle'
    at = fields.Many2one('viseo_atelier.viseo_atelier', 'Atelier')
    # atelier = fields.Text(related='at.atelier.value')
    name = fields.Text("Nom de la pont")