# # -*- coding: utf-8 -*-
#
from odoo import models, fields, api


class AdmReenrollment(models.Model):
    _inherit = 'adm.common.mixin'

    allow_paracetamol = fields.Boolean("Allow paracetamol")
    allow_ibuprofen = fields.Boolean("Allow Ibuprofen")
    allow_throat_lozenge = fields.Boolean("Throat lozenge")
    allow_tummy_antacid = fields.Boolean("Tummy antacid")
    allow_antihistamine_cream_syrup_allergic_reaction = fields.Boolean("Antihistamine cream and syrup for allergic reaction")
    allow_hydrocortisone_cream = fields.Boolean("Hydrocortisone cream")
    allow_muscle_sprain_gel_spray = fields.Boolean("Muscle sprain gel or spray")
