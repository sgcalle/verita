# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    force_currency_id = fields.Many2one('res.currency', 'Force Currency')

    @api.onchange('force_currency_id')
    @api.depends('force_currency_id', 'company_id', 'company_id.currency_id')
    def _compute_currency_id(self):
        super(ProductTemplate, self)._compute_currency_id()
        for template_id in self.filtered('force_currency_id'):
            template_id.currency_id = template_id.force_currency_id
