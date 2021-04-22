# -*- coding: utf-8 -*-
# from odoo import http


# class AdmCustomVerita(http.Controller):
#     @http.route('/adm_custom_verita/adm_custom_verita/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adm_custom_verita/adm_custom_verita/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('adm_custom_verita.listing', {
#             'root': '/adm_custom_verita/adm_custom_verita',
#             'objects': http.request.env['adm_custom_verita.adm_custom_verita'].search([]),
#         })

#     @http.route('/adm_custom_verita/adm_custom_verita/objects/<model("adm_custom_verita.adm_custom_verita"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adm_custom_verita.object', {
#             'object': obj
#         })
