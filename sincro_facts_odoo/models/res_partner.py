# -*- coding: utf-8 -*-
from odoo import models, fields, _, api, exceptions


class Contact(models.Model):
    """ We inherit to enable School features for contacts """

    _inherit = "res.partner"

    import_log_ids = fields.One2many("sincro_facts_odoo.log", "partner_id")