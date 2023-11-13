# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class ViseoCautionBank(models.Model):
    _name = 'viseo.caution.bank'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Caution bancaire'
    

    name = fields.Char()
    po_ids = fields.Many2many('sale.order', string='Devis')
    amount_totals= fields.Float('Total HT', compute='_compute_total_purchase_amount')
    bank = fields.Many2one('res.bank', 'Banque')
    payment = fields.Selection(string="Type de payement", selection=[
        ('ch_b','Chèque bancaire'),
        ('ct_b','Caution bancaire'),
        ('ch_n','Chèque normal'),
        
    ],default='ch_b', copy=False)
    status = fields.Selection(string="Etat", selection=[
        ('new','Demande'),
        ('waiting','En cours'),
        ('accepted','Validé'),
        ('refused', 'Refusé'),
        ('canceled','Annulée')
    ], default="new", copy=False)
    expire_date = fields.Date('Date d\'expiration', required=True, default=datetime.datetime.today())
    
    
    def _compute_total_purchase_amount(self):
        if self.po_ids:
            amount_totals = sum(self.po_ids.mapped('amount_untaxed'))
            self.amount_totals = amount_totals
        else:
            self.amount_totals = 0
            
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('viseo.caution.bank') or '/'
        return super(ViseoCautionBank, self).create(vals)
    
