# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    reenrollment_ids = fields.One2many('adm.reenrollment', 'responsible_user_ids')