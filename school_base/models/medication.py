"""
Created on Feb 18, 2020

@author: LuisMora
"""
from odoo import models, fields


class SchoolBaseMedicalMedication(models.Model):
    _name = 'school_base.medical_medication'
    _description = "Medical medication"

    name = fields.Char("Name")
    comment = fields.Char("Comment")
    prescription = fields.Char()
    self_administer = fields.Boolean()
    dose = fields.Char()
    type = fields.Selection(
        [('otc', "OTC"),
         ('prescription_drug', "Prescription drug")],
        required=True, default='otc')

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)
