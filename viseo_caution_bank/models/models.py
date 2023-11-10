# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class viseo_caution_bank(models.Model):
#     _name = 'viseo_caution_bank.viseo_caution_bank'
#     _description = 'viseo_caution_bank.viseo_caution_bank'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
