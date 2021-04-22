# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    """  Settings for school base module """
    _inherit = "res.config.settings"

    tuition_plan_categ_id = fields.Many2one(
        'product.category', config_parameter='adm.tuition_plan_categ_id')
    food_plan_categ_id = fields.Many2one(
        'product.category', config_parameter='adm.food_plan_categ_id')
    shadow_teacher_categ_id = fields.Many2one(
        'product.category', config_parameter='adm.shadow_teacher_categ_id')
