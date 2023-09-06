from odoo import models, fields, api


class place_vehicle(models.Model):
    _name= 'place_vehicle.place_vehicle'

    at = fields.Many2one('viseo_atelier.viseo_atelier', 'Atelier')
    # atelier = fields.Selection(related='at.atelier')
    name = fields.Text("Numero de place")