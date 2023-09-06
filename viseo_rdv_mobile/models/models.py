# -*- coding: utf-8 -*-
import datetime

from docutils.nodes import emphasis

from odoo import models, fields, api
from odoo.odoo.osv import expression
from odoo.exceptions import AccessError, UserError, ValidationError


class viseo_rdv_mobile(models.Model):
    _name = 'viseo_rdv_mobile.viseo_rdv_mobile'
    _inherit = ['mail.thread', 'mail.activity.mixin']

#     _description = 'viseo_rdv_mobile.viseo_rdv_mobile'
#     _inherit ='fleet.vehicle'
    name=fields.Char(string="RDV")
    date_rdv= fields.Datetime(default=fields.Datetime.now)
    date_start=fields.Datetime(default=datetime.datetime.now(), invisible=True, string="Début")
    date_stop= fields.Datetime(default=datetime.datetime.now()+datetime.timedelta(hours=1), invisible=True, string="Fin")
    place = fields.Many2one('place_vehicle.place_vehicle', 'Numero de place' ,domain="[('at.id','=',ate)]",copy=False)
    pont = fields.Many2one('pont_vehicle.pont_vehicle', 'Numero de pont', domain="[('at.id','=',ate)]",copy=False)
    choice = fields.Selection(string="Emplacement", selection=[
        ('pl','Place'),
        ('pt','Pont'),
    ], default="pl")
    # mecano = fields.Many2one('hr.employee', 'Mecano')
    #company_id = fields.Many2one('res.company', 'Company')
    user_id = fields.Many2one('res.users', string="Demandeur", readonly=True, default=lambda self: self.env.user.id)
    mecano = fields.Many2one('hr.employee', 'Mecano',domain="['|', ('company_id', '=', False), ('company_id.name', '=', 'Ocean Trade')]", copy=False)
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicules')
    user_resp = fields.Boolean(compute='test_user')
    # color = fields.Integer(string="Color", related='state_id.color')
    ate = fields.Many2one('viseo_atelier.viseo_atelier', string="Atelier", group_expand="_read_group_atelier_ids")

    responsable_id = fields.Many2many('res.users',string="Responsable de l'atelier", related='ate.risponsable_id')
    nom = fields.Many2one(related='ate.name')
    state = fields.Selection(string="Type RDV",selection=[
        ('entretient','Entretien'),
        ('revision','Révision'),
        ('achat', 'Achats')
    ])
    staten = fields.Many2one('type_rdv.type_rdv', string='Type de Rendez-vous')
    note = fields.Text(string='Messages', required=True)
    # status_id=fields.Many2one('rdv.state', string="Statut")
    color=fields.Integer(default=1)
    status = fields.Selection(string="Etat", selection=[
        ('new','Demande'),
        ('draft','Broullion'),
        ('accepted','Validé'),
        ('refused', 'Refusé'),
        ('canceled','Annulée')
    ], default="new", copy=False)

    can_validate = fields.Boolean(compute='_check_validator')
    #rdv_date = fields.Datetime(string="Date et heure")

    @api.constrains('date_start', 'date_stop', 'status', 'ate')
    def _check_date(self):
        domains = [[
            ('date_start', '<', reservation.date_stop),
            ('date_stop', '>', reservation.date_start),
            ('mecano', '=', reservation.mecano.id),
            ('id', '!=', reservation.id),
        ] for reservation in self.filtered('mecano')]
        domain = expression.AND([
            [('status', 'not in', ['canceled', 'refused'])],
            expression.OR(domains)
        ])
        if self.search_count(domain):
            raise ValidationError(('Vous ne pouvez pas avoir la même mecano qui se superposent à la même période'))
        else:
            domains = [[
                ('date_start', '<', reservation.date_stop),
                ('date_stop', '>', reservation.date_start),
                ('place', '=', reservation.place.id),
                ('id', '!=', reservation.id),
            ] for reservation in self.filtered('place')]
            domain = expression.AND([
                [('status', 'not in', ['canceled', 'refused'])],
                expression.OR(domains)
            ])
            if self.search_count(domain):
                raise ValidationError(('La place est déjà pris à cette même période'))



    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('viseo_rdv_mobile.viseo_rdv_mobile') or '/'
        return super(viseo_rdv_mobile,self).create(vals)

    # def rdvcreate(self):
    #

    def ask_rdv_vehicle(self):
        #to_subscribe = self.risponsable_id
        #substitute_leave = self.env['ir.module.module'].sudo().search([('name','=','viseo_substitute_leave'),('state','=','installed')])





        # if substitute_leave:
        #     if to_subscribe.substitute_id:
        #         to_subscribe |= to_subscribe.substitute_id
        return self.write({'status': 'draft','color':4})
    
    @api.model
    def _read_group_atelier_ids(self, atelier, domain, order):
        if self._context.get('restrict_rdv'):
            return atelier
        all_atelier = atelier.search([], order='name desc')
        return all_atelier

    def test_user(self):
        user = self.env.user.id
        resp_id = self.responsable_id.ids
        resp_id.append(2)
        if user in resp_id:
            self.user_resp = True
        else:
            self.user_resp = False

    def _check_validator(self):
        # self._check_can_cancel()
        current_user = self.env.user
        responsables = self.responsable_id.ids
        responsables.append(2)
        substitute_leave = self.env['ir.module.module'].sudo().search([('name','=','viseo_substitute_leave'),('state','=','installed')])
        if substitute_leave:
            if self.responsable_id.substitute_id:
                substitute_responsable = self.responsable_id.substitute_id.ids
                responsables = responsables + substitute_responsable
        if current_user.id in responsables:
            self.can_validate = True
        else:
            self.can_validate = False

    def action_validate(self):
        mecano = self.mecano
        place = self.place
        pont = self.pont
        date_start = self.date_start
        choice = self.choice
        if choice == 'pl':
            if mecano.id==False or place.id==False :
                raise ValidationError(('Veuillez ajouter un mecano ou une place'))
            else:
                records = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].search(
                    [('status', '=', 'accepted'), ('id', '<', self.id)])
                if records:
                    for record in records:
                        if record.mecano.id == mecano.id and record.date_start == date_start:
                            raise ValidationError(('Vous ne pouvez pas avoir la mécano à la même période'))
                        else:
                            print("Validé Mecano :", mecano.id)
                            return self.write({'status': 'accepted', 'color': 5})
                else:
                    return self.write({'status': 'accepted', 'color': 5})
        elif choice == 'pt':
            if mecano.id==False or pont.id == False:
                raise ValidationError(('Veuillez ajouter un mecano ou un pont'))
            else:
                records = self.env['viseo_rdv_mobile.viseo_rdv_mobile'].search([('status','=','accepted'),('id','<',self.id)])
                if records:
                    for record in records:
                        if record.mecano.id == mecano.id and record.date_start == date_start:
                            raise ValidationError(('Vous ne pouvez pas avoir la mécano à la même période'))
                        else:
                            print("Validé Mecano :", mecano.id)
                            return self.write({'status': 'accepted','color' :5 })
                else:
                    return self.write({'status': 'accepted', 'color': 5})

class Atelier(models.Model):
    _name= 'viseo_atelier.viseo_atelier'
    # name=fields.Char(string='Atelier(s)')
    name = fields.Many2one('fleet.workshop.type',string='Type Atelier')
    risponsable_id = fields.Many2many('res.users', string='Responsable(s)')

class RdvState(models.Model):
    _name = 'rdv.state'

    name = fields.Char(string='Etat')
    color = fields.Integer(string="Color")



class TypeRDV(models.Model):
    _name = 'type.rdv'
    name = fields.Char(string='Type Rendez-vous')
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
