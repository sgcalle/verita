# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerLegalDocuments(http.Controller):
#     @http.route('/partner_legal_documents/partner_legal_documents/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_legal_documents/partner_legal_documents/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_legal_documents.listing', {
#             'root': '/partner_legal_documents/partner_legal_documents',
#             'objects': http.request.env['partner_legal_documents.partner_legal_documents'].search([]),
#         })

#     @http.route('/partner_legal_documents/partner_legal_documents/objects/<model("partner_legal_documents.partner_legal_documents"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_legal_documents.object', {
#             'object': obj
#         })
