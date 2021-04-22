# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AdmReenrollmentPage(models.Model):
    _name = 'adm.reenrollment.page'
    _description = "Reenrollment page"

    active = fields.Boolean(default=True)
    sequence = fields.Integer(default='-1')
    name = fields.Char(translate=True)
    url = fields.Char()
    internal_reference = fields.Char()
    website_id = fields.Many2one('website')
    previous_page_id = fields.Many2one('adm.reenrollment.page')
    next_page_id = fields.Many2one('adm.reenrollment.page')
    view_template_id = fields.Many2one('ir.ui.view')
    parent_id = fields.Many2one('adm.reenrollment.page')
    child_ids = fields.One2many('adm.reenrollment.page', 'parent_id')

    _sql_constraints = [
        ('adm_reenrollment_page_internal_reference',
         'unique (internal_reference, website_id)',
         "The internal reference should be unique by website"),
        ]

    @api.model
    def find_by_reference(self, reference):
        return self.search([('internal_reference', '=', reference)])[:1]
