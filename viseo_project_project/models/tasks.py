
from odoo import fields, models, api, http



class PojectTaskNew (models.Model):
    _inherit = 'viseo.project.task'


    amount = fields.Float("Montant")
    progress_bar = fields.Integer(compute='_compute_progress')

    # @api.model
    # def search_filter_categories(self, project_id):
    #     project = self.env['project.project']
    #     projects = project.search([('id', 'child_of', project_id)]).ids
    #     return {'list_project' : projects}

    @api.model
    def search_panel_select_range(self, field_name, project_id=None):
        all_projects = super(PojectTaskNew, self).search_panel_select_range(field_name)
        if project_id and self._name == 'viseo.project.task' and field_name == 'project_id':
            project = self.env['viseo.project.project']
            list_of_projects = project.search([('id', 'child_of', project_id)]).ids
            new_list_of_projects = [sub for sub in all_projects['values'] if sub['id'] in list_of_projects]
            all_projects['values'] = new_list_of_projects
        return all_projects


    @api.depends('planned_date_begin', 'planned_date_end')
    def _compute_progress(self):
        for rec in self:
            rec.progress_bar = 0
            if rec.planned_date_begin and rec.planned_date_end:
                total_days = rec.planned_date_end - rec.planned_date_begin
                progress = rec.planned_date_end - fields.Datetime.now()
                try:
                    percentage = (total_days.days - progress.days) * 100 / total_days.days
                    rec.progress_bar = round(percentage)
                except ZeroDivisionError:
                    rec.progress_bar = 0



