# -*- coding: utf-8 -*-

from odoo import models, fields, api


class viseo_analytic(models.Model):
    _name = 'viseo_analytic.viseo_analytic'
#     _description = 'viseo_analytic.viseo_analytic'
    #_inherit = 'account.move'
    name = fields.Char(default='Nouveau')
    start_date = fields.Date('Date de début')
    end_date = fields.Date('Date de fin')
    supplier_id = fields.Many2one('res.partner', 'Fournisseur')
    amount_total = fields.Float('Total')
    percent = fields.Float('Pourcentage')
    departement_id = fields.Many2one('account.department', 'Département')
    analytic_count = fields.Integer('Analytique', default=0)
    html_content = fields.Html('Contenu html')
    famille = fields.Many2one('famille.analytique', string="Famille analytique")

    def _read_depart_group(self):
        test = self.env['account.department'].sudo().search([])
        print(test)
        return test


    def _render_table(self):
        departments = self._read_depart_group()
        print(departments)
        return {
            'departements': departments
        }
    @api.model
    def create(self, sequence):
        sequence['name'] = self.env['ir.sequence'].next_by_code('viseo_analytic.viseo_analytic') or '/'

        return super(viseo_analytic, self).create(sequence)
    
    def action_pivot_view_test(self):
        print('TEst')
        self.ensure_one()
        return {
             'type': 'ir.actions.act_window',
             'name': 'Analytique viseo',
             'view_mode': 'pivot',
             'res_model': 'viseo_analytic.viseo_analytic',
             #'domain': [('vehicle_id', '=', self.id)],
             #'context': {'default_driver_company': self.true_driver.id, 'default_driver_other': self.other_driver, 'default_vehicle_id': self.id}
         }
        
    def read_group_department_ids(self, department, domain, order):
        if self._context.get('restrict_rdv'):
            return department
        all_atelier = department.search(['account_department'], order='name desc')
        print('atelier: ',all_atelier)
        return all_atelier



    def action_afficher_template(self):
        #
        # test = self.env['account.department'].sudo().search([])
        # for t in test:
        #     print(t.name)
        return {
            'name': 'Affichage du Template',
            'type': 'ir.actions.act_window',
            'res_model': 'viseo_analytic.viseo_analytic',
            'view_mode': 'form',
            'view_id': self.env.ref('viseo_analytic_viseo.view_my_template').id,
            # Remplacez 'my_module.view_my_template' par l'ID de votre vue template
            'target': 'current',
        }
        

    
    @api.onchange('supplier_id')
    def compute_invoice_total(self):
        # Recherche des factures du fournisseur dans la période spécifiée
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.supplier_id.id),
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('type', '=', 'in_invoice'),  # Factures fournisseur
            ('state', '=', 'posted'),  # Factures validées
        ])

        # Calcul de la somme totale des factures
        total_amount = sum(invoice.amount_total for invoice in invoices)

        
        self.amount_total= total_amount



        

class AnalytiqueFamille(models.Model):
    _name = 'famille.analytique'
    
    
    name = fields.Char('Famille')
    
class Analytiquefamille(models.Model):
    _inherit = 'purchase.order'
    
    
    famille = fields.Many2one('famille.analytique')
        
   
    
    
    
    
    
    

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
# {
#             'name': 'Somme des factures du fournisseur',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'viseo_analytic.viseo_analytic',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'target': 'new',
#             'context': {'default_start_date': self.start_date,
#                         'default_end_date': self.end_date,
#                         'default_supplier_id': self.supplier_id.id,
#                         'default_total_amount': total_amount,
#                         'amout_total':total_amount
#                         },
#         },
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    
        
