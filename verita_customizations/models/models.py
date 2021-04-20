# # -*- coding: utf-8 -*-
#
# from odoo import models, fields, api
#
#
# class Foo(models.Model):
#     _name = 'module.Foo'
#     _description = 'Foo'
#
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
#
#
# class Boo(models.Model):
#     _inherit = 'module.Foo'
#     _description = 'Boo'
#
#     name = fields.Char()
#     value3 = fields.Integer()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = record.value3 * record.value
