# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, _
from odoo.tools import safe_eval

SELECT_REENROLLMENT_STATUS = [
    ("open", "Open"),
    ("finished", "Finished"),
    ("withdrawn", "Withdrawn"),
    ("rejected", "Rejected"),
    ("blocked", "Blocked"),
    ]


class AdmReenrollmentTask(models.Model):
    _name = 'adm.reenrollment.task'
    _description = "Reenrollment task"

    name = fields.Char()
    stage_id = fields.Many2one('adm.reenrollment.stage')


class AdmReenrollmentStage(models.Model):
    _name = 'adm.reenrollment.stage'
    _order = 'sequence'
    _description = "Reenrollment stage"

    name = fields.Char("Status Name")
    description = fields.Text("Description")
    sequence = fields.Integer(readonly=True, default=-1)
    fold = fields.Boolean("Fold")
    type = fields.Selection([
            ("start", "Start"),
            ("stage", "Stage"),
            ("returning", "Returning"),
            ("not_returning", "Not returning"),
        ], default='stage')

    task_ids = fields.One2many('adm.reenrollment.task', 'stage_id')

    reenrollment_status_to_facts = fields.Selection(SELECT_REENROLLMENT_STATUS, string="Reenrollment Status to FACTS")
    sub_status_to_facts = fields.Many2one("school_base.enrollment.sub_status", string="Sub Status to FACTS")
    import_to_facts = fields.Boolean()


class AdmReenrollment(models.Model):
    """ Reenrollment packages """

    ######################
    # Private Attributes #
    ######################
    _name = 'adm.reenrollment'
    _description = "Reenrollment"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    active = fields.Boolean(default=True)
    log_ids = fields.One2many('adm.reenrollment.log', 'reenrollment_id',
                              string="Logs")
    partner_id = fields.Many2one('res.partner', string='Student')
    name = fields.Char(string="Name", related="partner_id.name")

    stage_id = fields.Many2one('adm.reenrollment.stage', 'Stage',
                               group_expand="_read_group_stage_ids")
    stage_task_ids = fields.One2many('adm.reenrollment.task',
                                     related='stage_id.task_ids')

    grade_level_id = fields.Many2one('school_base.grade_level',
                                     string="Current Grade level")
    school_year_id = fields.Many2one('school_base.school_year',
                                     string=_("Reenrollment school year"))

    user_id = fields.Many2one('res.users')

    tuition_plan_id = fields.Many2one('tuition.plan')

    # Demographics
    email = fields.Char(string="Email", related="partner_id.email", index=True)
    mobile = fields.Char(string="Phone", related="partner_id.mobile")
    phone = fields.Char(string="Home phone", related="partner_id.phone")
    image = fields.Binary("Applicant´s Photo", related="partner_id.image_1920")

    # Family
    family_ids = fields.Many2many(related='partner_id.family_ids')
    family_res_id = fields.Integer("Family ID")

    # Responsible
    user_access_ids = fields.One2many('adm.reenrollment.user.access', 'reenrollment_id')
    responsible_user_ids = fields.Many2many('res.users', compute="_compute_responsible_users", string="Responsible User")
    current_user_access_id = fields.Many2one('adm.reenrollment.user.access',
        compute='compute_current_user_access')
    responsible_user_id = fields.Many2one('res.users')
    custody_user_ids = fields.Many2many(
        'res.users',
        help="All the users here will receive "
             "a mail to go to complete the reenrollment")
    # responsible_email = fields.Char(related='responsible_user_id.email')

    # Medical
    doctor_name = fields.Char(
        "Doctor name", related='partner_id.doctor_name', readonly=False)
    doctor_phone = fields.Char(
        "Doctor phone", related='partner_id.doctor_phone', readonly=False)
    doctor_address = fields.Char(
        "Doctor Direction", related='partner_id.doctor_address',
        readonly=False)
    hospital = fields.Char(
        "Hospital", related='partner_id.hospital', readonly=False)
    hospital_address = fields.Char(
        "Hospital Address", related='partner_id.hospital_address',
        readonly=False)
    permission_to_treat = fields.Boolean(
        "Permission To Treat", related='partner_id.permission_to_treat',
        readonly=False)
    blood_type = fields.Char(
        "Blood Type", related='partner_id.blood_type', readonly=False)

    medical_allergies_ids = fields.One2many(
        string="Allergies", related="partner_id.medical_allergies_ids",
        readonly=False)
    medical_conditions_ids = fields.One2many(
        string="Conditions", related="partner_id.medical_conditions_ids",
        readonly=False)
    medical_medications_ids = fields.One2many(
        string="Medications", related="partner_id.medical_medications_ids",
        readonly=False)

    responsible_school_status = fields.Selection(
        [('parent', _("Parent")), ('staff', _("Staff"))],
        string="Responsible school status")

    partner_guardian1 = fields.Many2one('res.partner')
    partner_guardian2 = fields.Many2one('res.partner')

    # Reenrollment data
    is_returning = fields.Boolean(
        help=_("Will the student will return to the school?"))
    next_grade_level_id = fields.Many2one('school_base.grade_level',
                                          "Next grade level")

    student_id_documentation_file = fields.Binary(
        related='partner_id.id_documentation_file', string="ID Documentation",
        readonly=False)
    student_id_documentation_file_name = fields.Char(
        related='partner_id.id_documentation_file_name', readonly=False)

    guardian1_id_documentation_file = fields.Binary(
        related='partner_guardian1.id_documentation_file',
        string="Guardian 1 ID Documentation", readonly=False)
    guardian1_id_documentation_file_name = fields.Char(
        related='partner_guardian1.id_documentation_file_name', readonly=False)

    guardian2_id_documentation_file = fields.Binary(
        related='partner_guardian2.id_documentation_file',
        string="Guardian 2 ID Documentation", readonly=False)
    guardian2_id_documentation_file_name = fields.Char(
        related='partner_guardian2.id_documentation_file_name', readonly=False)

    # Location
    partner_home_address_id = fields.Many2one(
        'school_base.home_address', related='partner_id.home_address_id')

    # Relationships
    partner_relationship_ids = fields.Many2many('school_base.relationship', related='partner_id.self_relationship_ids')

    # Documentation
    contract_file = fields.Binary(attachment=True)

    # Fee
    registration_fee_amount = fields.Float()
    reenrollment_deposit_amount = fields.Float()

    ##############################
    # Compute and search methods #
    ##############################
    def _compute_responsible_users(self):
        for reenrollment in self:
            reenrollment.responsible_user_ids = reenrollment.mapped('user_access_ids.user_id')

    def compute_current_user_access(self):
        for reenrollment in self:
            user_access = reenrollment.user_access_ids.filtered(
                lambda us: us.user_id == self.env.user
                ).sorted('create_date', reverse=True)
            reenrollment.current_user_access_id = user_access[:1]

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['adm.reenrollment.stage'].search([])

    @api.model
    def create(self, vals):
        reenrollment_id = super(AdmReenrollment, self).create(vals)

        # Contract default file
        reenrollment_id.regenerate_contract_pdf()

        return reenrollment_id

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
    def regenerate_contract_pdf(self):
        for reenrollment_id in self:
            pdf_binary = self.env.ref('adm_reenrollment.report_contract_reenrollment').render_qweb_pdf(reenrollment_id.ids)
            b64_pdf = base64.b64encode(pdf_binary[0])
            reenrollment_id.contract_file = b64_pdf

    def get_required_fields(self):
        # First we get the all the fields
        config_parameter = self.env['ir.config_parameter'].sudo()
        reenrollment_required_fields_str = config_parameter.get_param('adm_reenrollment_required_field_ids', '')
        reenrollment_required_fields = [int(e) for e in reenrollment_required_fields_str.split(',') if e.isdigit()]
        required_field_ids = self.env['adm_reenrollment.fields.settings'].sudo().browse(reenrollment_required_fields)

        # Then we filter by the field domain
        filtered_required_fields_ids = self.env['adm_reenrollment.fields.settings'].sudo()
        for required_field_id in required_field_ids:
            if required_field_id.apply_domain_in_records(self):
                filtered_required_fields_ids += required_field_id

        return filtered_required_fields_ids

    def get_optional_fields(self):
        reenrollment_optional_fields_str = self.env['ir.config_parameter'].sudo().get_param('adm_reenrollment_optional_field_ids', '')
        reenrollment_optional_fields = [int(e) for e in reenrollment_optional_fields_str.split(',') if e.isdigit()]
        optional_field_ids = self.env['adm_reenrollment.fields.settings'].sudo().browse(reenrollment_optional_fields)

        filtered_optional_field_ids = self.env['adm_reenrollment.fields.settings'].sudo()
        for required_field_id in optional_field_ids:
            if required_field_id.apply_domain_in_records(self):
                filtered_optional_field_ids += optional_field_ids

        return filtered_optional_field_ids


class AdmReenrollmentLog(models.Model):
    """ Reenrollment logs """

    ######################
    # Private Attributes #
    ######################
    _name = 'adm.reenrollment.log'
    _description = "Reenrollment log"
    _order = 'timestamp desc'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char()
    timestamp = fields.Datetime()

    user_id = fields.Many2one('res.users')

    user_agent = fields.Text()

    ip_address = fields.Char()
    json_values = fields.Text()

    reenrollment_id = fields.Many2one('adm.reenrollment', ondelete='SET NULL')

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


class AdmreenrollmentUserAccess(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = 'adm.reenrollment.user.access'
    _description = "reenrollment user access"

    ######################
    # Fields declaration #
    ######################
    reenrollment_id = fields.Many2one('adm.reenrollment', required=True)
    user_id = fields.Many2one('res.users', required=True)
    family_id = fields.Many2one('res.partner', required=True)

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
