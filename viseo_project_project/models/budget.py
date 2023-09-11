from odoo import fields, models, api


class ProjectBudget(models.Model):
    _name = 'project.budget'
    _description = 'Budget de projets'

    viseo_project_id = fields.Many2one('viseo.project.project', string='Projet')
    family_group = fields.Many2one('project.family.group', string='Groupe de famille')
    amount = fields.Float(string='Montant HT', required=True)
    description = fields.Char(string='Déscription')
    observation = fields.Char(string='Obsérvation')
    is_valid = fields.Boolean(string='Validé', default=False)
    

class ProjectFamilyGroup(models.Model):
    _name = 'project.family.group'

    name = fields.Char('Nom')
