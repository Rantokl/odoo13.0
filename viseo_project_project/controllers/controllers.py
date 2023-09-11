# -*- coding: utf-8 -*-
# from odoo import http


# class ViseoProjectProject(http.Controller):
#     @http.route('/viseo_project_project/viseo_project_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viseo_project_project/viseo_project_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('viseo_project_project.listing', {
#             'root': '/viseo_project_project/viseo_project_project',
#             'objects': http.request.env['viseo_project_project.viseo_project_project'].search([]),
#         })

#     @http.route('/viseo_project_project/viseo_project_project/objects/<model("viseo_project_project.viseo_project_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viseo_project_project.object', {
#             'object': obj
#         })
