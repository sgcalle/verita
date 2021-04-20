# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# todo: Move the common fields here
# We need to move te common fields in inquiry, application,
# future enrollment model and reenrollment right here


class AdmCommonMixin(models.Model):
    """ Common model used for inquiry, application, enrollment and reenrollment """

    ######################
    # Private Attributes #
    ######################
    _name = 'adm.common.mixin'
    _description = "Common mixin used for inquiry, application, enrollment and reenrollment"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
