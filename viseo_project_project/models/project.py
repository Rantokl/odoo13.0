from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
import numpy as np

class ProjectProjectViseo(models.Model):
    _inherit = 'viseo.project.project'


    # edit_hide_css = fields.Html(string='CSS', sanitize=False, compute='_compute_edit_hide_css')
    #
    #
    # def _compute_edit_hide_css(self):
    #     for rec in self:
    #         if rec.state in ['done'] and self.env.user.login != 'admin':
    #             rec.edit_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
    #         else:
    #             rec.edit_hide_css = False

    parent_id = fields.Many2one('viseo.project.project', string='Projet parent', ondelete='cascade')
    child_ids = fields.One2many('viseo.project.project', 'parent_id', string='Sous projet(s)')
    subproject_count = fields.Integer("Sub-task count", compute='_compute_subproject_count')
    purchase_order_ids = fields.One2many('purchase.order', 'viseo_project_id', string="Achats")
    sale_order_ids = fields.One2many('sale.order', 'viseo_project_id', string="Ventes")
    internal_request_ids = fields.One2many('internal.request', 'viseo_project_id', string="CS")
    expense_sheet_ids = fields.One2many('hr.expense', 'viseo_project_id', string="Ndf")
    cost_ids = fields.One2many('project.cost', 'viseo_project_id', string="Autres coûts")
    budget_ids = fields.One2many('project.budget', 'viseo_project_id', string="Budgets")
    budget_purpose = fields.Monetary(string='Budget à allouer', compute='_compute_budget_purpose')
    total_expense = fields.Float(string='Dépenses Total', tracking=True, compute='_compute_expenses')
    total_po = fields.Float(string='Prévisionnel', tracking=True, compute='_compute_expense_po')
    total_validate = fields.Float(string='Validé', tracking=True, compute='_compute_expense_po')
    total_paid = fields.Float(string='Payé', tracking=True, compute='_compute_expense_po')
    start_date = fields.Datetime(string="Date debut")
    end_date = fields.Datetime(string="Date fin")
    duration = fields.Integer(string=u"Durée", default=0)
    duration_unit = fields.Selection([("open_days", "Jours ouvrés"), ("days", "Jours"), ("weeks", "Semaines"), ("months", "Mois"), ("years", "Années")],
                                     string="Unit", required=True)
    # is_project_viseo = fields.Boolean(default=False)
    # compute = "_compute_duration_project",
    # duration_condition = fields.Selection([("journey", "Journée"), ('day', 'Jours'), ('week', 'Semaines'), ('month', 'Mois'), ('year','Années')],
    #                                     string="Condition de location", default='day')
    vente = fields.Selection([("-", "- Vente"), ("+", "Vente")], default='-')
    po = fields.Selection([("-", "- PO"), ("+", "+ PO")], default='+')
    cs = fields.Selection([("-", "- CS"), ("+", "+ CS")], default='+')
    ndf = fields.Selection([("-", "- Ndf"), ("+", "+ Ndf")], default='+')



    # @api.model
    # def create(self, vals):
    #     print(self._context)
    #     action_id = self._context.get('action')
    #     print("**************")
    #     print(action_id)
    #     return super(ProjectProjectViseo, self).create(vals)

    @api.depends('budget_ids')
    def _compute_budget_purpose(self):
        for budget in self:
            budget.budget_purpose = sum(budget.budget_ids.filtered(lambda x: x.is_valid == True).mapped('amount'))

    def valid_expenses(self):
        if bool(self.budget_ids):
            for budget in self.budget_ids:
                if not budget.is_valid:
                    budget.is_valid = True
            budget_purpose = sum(self.budget_ids.filtered(lambda x: x.is_valid == True).mapped('amount'))
            body_message = (("<div class='col-xs-6'>"
                              "<ul>"
                              "<li><i>Budget validé</i></li>"
                              "<li>%s</li>"
                              "</ul>"
                              "</div>")%(budget_purpose))
            self.message_post(body=body_message)


    def _compute_expense_po(self):
        for po in self:
            # other_cost = pj.cost_ids
            purchases = po.purchase_order_ids
            purchase_valid = po.purchase_order_ids.filtered(lambda po: po.state in ['purchase', 'done'])
            purchase_invoiced = po.purchase_order_ids.filtered(lambda po: po.state in ['purchase', 'done'] and po.invoice_status == 'invoiced')
            invoices = self.env['account.move'].search([('linked_po', 'in', purchase_invoiced.ids), ('invoice_payment_state', '=', 'paid')])
            po.total_po = sum(purchases.mapped('amount_total'))
            po.total_validate = sum(purchase_valid.mapped('amount_total'))
            po.total_paid = sum(invoices.mapped('amount_total'))

    def _compute_expenses(self):
        expenses = 0
        for pj in self:
            other_cost = pj.cost_ids
            purchase = pj.purchase_order_ids.filtered(lambda po: po.state in ['purchase', 'done'])
            request = pj.internal_request_ids.filtered(lambda r: r.state == 'done')
            expense = pj.expense_sheet_ids.filtered(lambda r: r.state == 'done')
            if bool(other_cost):
                expenses = sum(other_cost.mapped('cost_amount'))
            if bool(purchase):
                expenses += sum(purchase.mapped('amount_total'))
            if bool(request):
                expenses += sum(request.mapped('amount_subtotal'))
            if bool(expense):
                expenses += sum(expense.mapped('total_amount'))
            pj.total_expense = expenses

    @api.onchange('po')
    def onchange_po(self):
        purchase = self.purchase_order_ids.filtered(lambda po: po.state in ['purchase', 'done'])
        total = sum(purchase.mapped('amount_total'))
        if self.po == '-':
            self.total_expense = self.total_expense - total
        else:
            self.total_expense = self.total_expense + total

    @api.onchange('vente')
    def onchange_vente(self):
        sale = self.sale_order_ids.filtered(lambda v: v.state in ['sale', 'done'])
        total = sum(sale.mapped('amount_untaxed'))
        if self.vente == '+':
            self.total_expense = self.total_expense + total
        else:
            self.total_expense = self.total_expense - total

    @api.onchange('ndf')
    def onchange_ndf(self):
        ndf = self.expense_sheet_ids.filtered(lambda v: v.state in ['done'])
        total = sum(ndf.mapped('total_amount'))
        if self.ndf == '-':
            self.total_expense = self.total_expense - total
        else:
            self.total_expense = self.total_expense + total

    @api.onchange('cs')
    def onchange_cs(self):
        cs = self.internal_request_ids.filtered(lambda c: c.state in ['done'])
        total = sum(cs.mapped('amount_subtotal'))
        if self.cs == '-':
            self.total_expense = self.total_expense - total
        else:
            self.total_expense = self.total_expense + total

    def compute_days_weeks(self, date, no_of_days):
        """This methods return future date by adding given number of days excluding
         weekends"""
        future_date = date + timedelta(no_of_days)
        no_of_busy_days = int(np.busday_count(date.date(), future_date.date()))
        if no_of_busy_days != no_of_days:
            extend_future_date_by = no_of_days - no_of_busy_days
            future_date = future_date + timedelta(extend_future_date_by)
        return future_date

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.duration:
            if self.duration_unit == 'open_days':
                # self.compute_days_weeks(self.start_date, self.duration)
                self.end_date = self.compute_days_weeks(self.start_date, self.duration)
            elif self.duration_unit == 'days':
                self.end_date = self.start_date + timedelta(days=self.duration)
            elif self.duration_unit == 'weeks':
                self.end_date = self.start_date + timedelta(weeks=self.duration)
            elif self.duration_unit == 'months':
                self.end_date = self.start_date + relativedelta(months=self.duration)
            elif self.duration_unit == 'years':
                self.end_date = self.start_date + relativedelta(years=self.duration)

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.start_date and self.end_date:
            diff_date = self.end_date - self.start_date
            if self.duration_unit == 'open_days':
                days = np.busday_count(self.start_date.date(), self.end_date.date())
                self.duration = days
            elif self.duration_unit == 'days':
                self.duration = diff_date.days
            elif self.duration_unit == 'weeks':
                self.duration = diff_date.days / 7
            elif self.duration_unit == 'months':
                self.duration = diff_date.days / 30
            else:
                self.duration = diff_date.days / 365

    @api.onchange('duration_unit')
    def _compute_duration_project(self):
        '''To compute the duration unit (day, week, month, year) and the duration by the difference between two dates with its duration unit
        '''
        if self.duration > 0:
            if self.start_date:
                if self.duration_unit == 'open_days':
                    self.end_date = self.compute_days_weeks(self.start_date, self.duration)
                elif self.duration_unit == 'days':
                    self.end_date = self.start_date + timedelta(days=self.duration)
                elif self.duration_unit == 'weeks':
                    self.end_date = self.start_date + timedelta(weeks=self.duration)
                elif self.duration_unit == 'months':
                    self.end_date = self.start_date + relativedelta(months=self.duration)
                elif self.duration_unit == 'years':
                    self.end_date = self.start_date + relativedelta(years=self.duration)
            else:
                self.start_date = datetime.now()
                if self.duration_unit == 'open_days':
                    self.end_date = self.compute_days_weeks(self.start_date, self.duration)
                elif self.duration_unit == 'days':
                    self.end_date = self.start_date + timedelta(days=self.duration)
                elif self.duration_unit == 'weeks':
                    self.end_date = self.start_date + timedelta(weeks=self.duration)
                elif self.duration_unit == 'months':
                    self.end_date = self.start_date + relativedelta(months=self.duration)
                elif self.duration_unit == 'years':
                    self.end_date = self.start_date + relativedelta(years=self.duration)


    @api.onchange('duration')
    def onchange_duration(self):
        '''Set the end date compared with inserted duration
        '''
        # self._compute_duration_viseo()
        if self.start_date and self.duration > 0:
            if self.duration_unit == 'open_days':
                self.end_date = self.compute_days_weeks(self.start_date, self.duration)
            elif self.duration_unit == 'days':
                self.end_date = self.start_date + timedelta(days=self.duration)
            elif self.duration_unit == 'weeks':
                self.end_date = self.start_date + timedelta(weeks=self.duration)
            elif self.duration_unit == 'months':
                self.end_date = self.start_date + relativedelta(months=self.duration)
            elif self.duration_unit == 'years' :
                self.end_date = self.start_date + relativedelta(years=self.duration)
        # else:
        #     pass


    @api.depends('child_ids')
    def _compute_subproject_count(self):
        for project in self:
            if bool(project.child_ids):
                project.subproject_count = len(project.child_ids)
            else:
                project.subproject_count = 0

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id:
            self.has_parent = True
        else:
            self.has_parent = False

    has_parent = fields.Boolean(default=_onchange_parent_id)




class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    viseo_project_id = fields.Many2one('viseo.project.project',string="Projet lié")
    note_project = fields.Text(string="Motifs d'achat")
    family_group = fields.Many2one('project.family.group', string='Groupe de famille')

    @api.onchange('family_group')
    def _get_family_group_domain(self):
        if self.viseo_project_id:
            domain_family = self.viseo_project_id.budget_ids.mapped('family_group')
            domain = [('id', '=', domain_family.ids)]
        else:
            domain = [('id', '=', [])]
        return {'domain': {'family_group': domain}}

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    viseo_project_id = fields.Many2one('viseo.project.project',string="Projet")
    family_group = fields.Many2one('project.family.group', string='Groupe de famille')

    @api.onchange('family_group')
    def _get_family_group_domain(self):
        if self.viseo_project_id:
            domain_family = self.viseo_project_id.budget_ids.mapped('family_group')
            domain = [('id', '=', domain_family.ids)]
        else:
            domain = [('id', '=', [])]
        return {'domain': {'family_group': domain}}

class InternalRequest(models.Model):
    _inherit = 'internal.request'

    viseo_project_id = fields.Many2one('viseo.project.project',string="Projet")
    family_group = fields.Many2one('project.family.group', string='Groupe de famille')

    @api.onchange('family_group')
    def _get_family_group_domain(self):
        if self.viseo_project_id:
            domain_family = self.viseo_project_id.budget_ids.mapped('family_group')
            domain = [('id', '=', domain_family.ids)]
        else:
            domain = [('id', '=', [])]
        return {'domain': {'family_group': domain}}

class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense'

    viseo_project_id = fields.Many2one('viseo.project.project',string="Projet")
    family_group = fields.Many2one('project.family.group', string='Groupe de famille')

    @api.onchange('family_group')
    def _get_family_group_domain(self):
        if self.viseo_project_id:
            domain_family = self.viseo_project_id.budget_ids.mapped('family_group')
            domain = [('id', '=', domain_family.ids)]
        else:
            domain = [('id', '=', [])]
        return {'domain': {'family_group': domain}}


class OtherCost(models.Model):
    _name = 'project.cost'

    description = fields.Char('Description')
    cost_amount = fields.Float("Montant")
    viseo_project_id = fields.Many2one('viseo.project.project',string="Projet")


