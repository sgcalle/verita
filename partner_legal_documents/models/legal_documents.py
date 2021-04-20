# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    legal_document_ids = fields.One2many('pld.legal.document', 'partner_id')


class LegalDocument(models.Model):
    """ Legal Document """

    ######################
    # Private Attributes #
    ######################
    _name = 'pld.legal.document'
    _description = "Legal document"
    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    type_id = fields.Many2one('pld.legal.document.type')
    name = fields.Char(related='type_id.name')
    partner_id = fields.Many2one('res.partner')
    series = fields.Char()
    number = fields.Char()
    issued_by = fields.Char()

    expiration_date = fields.Date()
    issued_date = fields.Date()
    address = fields.Char()

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


class PldLegalDocumentType(models.Model):
    """ Legal Document Type """

    ######################
    # Private Attributes #
    ######################
    _name = 'pld.legal.document.type'
    _description = "Legal document type"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(translate=True)

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
