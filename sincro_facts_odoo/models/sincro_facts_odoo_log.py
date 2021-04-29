# -*- coding: utf-8 -*-
from odoo import models, fields, _, api, exceptions


class SincroFactsLog(models.Model):
    """ We inherit to enable School features for contacts """

    _name = "sincro_facts_odoo.log"
    _description = "Log about the importation of FACTS"

    name = fields.Char("Name")
    description = fields.Char("Description")
    partner_id = fields.Many2one("res.partner", "Contact")
