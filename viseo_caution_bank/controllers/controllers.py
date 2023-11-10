# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoCautionBank(http.Controller):
#     @http.route('/viseo_caution_bank/viseo_caution_bank/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_caution_bank/viseo_caution_bank/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_caution_bank.listing', {
#             'root': '/viseo_caution_bank/viseo_caution_bank',
#             'objects': http.request.env['viseo_caution_bank.viseo_caution_bank'].search([]),
#         })

#     @http.route('/viseo_caution_bank/viseo_caution_bank/objects/<model("viseo_caution_bank.viseo_caution_bank"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_caution_bank.object', {
#             'object': obj
#         })
