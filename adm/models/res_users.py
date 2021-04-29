# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    digital_signature = fields.Binary(string="Signature")
    application_ids = fields.One2many('adm.application', compute='compute_application_ids')

    def compute_application_ids(self):
        for user in self:
            user.application_ids = self.env['adm.application'].search([('responsible_user_ids', '=', user.id)])
