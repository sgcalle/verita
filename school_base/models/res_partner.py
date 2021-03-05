# -*- encoding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

from ..utils.commons import switch_statement

SELECT_PERSON_TYPES = [
    ("student", "Student"),
    ("parent", "Parent")
    ]

SELECT_COMPANY_TYPES = [
    ("person", "Person"),
    ("company", "Company/Family")
    ]

SELECT_STATUS_TYPES = [
    ("admissions", "Admissions"),
    ("enrolled", "Enrolled"),
    ("graduate", "Graduate"),
    ("inactive", "Inactive"),
    ("pre-enrolled", "Pre-Enrolled"),
    ("withdrawn", "Withdrawn"),
    ]

SELECT_REENROLLMENT_STATUS = [
    ("open", "Open"),
    ("finished", "Finished"),
    ("withdrawn", "Withdrawn"),
    ("rejected", "Rejected"),
    ("blocked", "Blocked"),
]


class Contact(models.Model):
    """ We inherit to enable School features for contacts """

    _inherit = "res.partner"

    # Overwritten fields
    # Name should be readonly
    allow_edit_student_name = fields.Boolean(
        compute="_retrieve_allow_name_edit_from_config")
    allow_edit_parent_name = fields.Boolean(
        compute="_retrieve_allow_name_edit_from_config")
    allow_edit_person_name = fields.Boolean(
        compute="_retrieve_allow_name_edit_from_config")

    is_name_edit_allowed = fields.Boolean(
        compute="_compute_allow_name_edition")

    def _retrieve_allow_name_edit_from_config(self):
        self.allow_edit_student_name = bool(
            self.env["ir.config_parameter"].sudo().get_param("school_base.allow_edit_student_name", False))
        self.allow_edit_parent_name = bool(
            self.env["ir.config_parameter"].sudo().get_param("school_base.allow_edit_parent_name", False))
        self.allow_edit_person_name = bool(
            self.env["ir.config_parameter"].sudo().get_param("school_base.allow_edit_person_name", False))

    @api.depends("allow_edit_student_name",
                 "allow_edit_parent_name",
                 "allow_edit_person_name",
                 "person_type")
    def _compute_allow_name_edition(self):
        for partner_id in self:
            # Sumulating switch statement
            partner_id.is_name_edit_allowed = switch_statement(cases={
                "default": partner_id.allow_edit_person_name,
                "parent": partner_id.allow_edit_parent_name,
                "student": partner_id.allow_edit_student_name,
                }, value=partner_id.person_type)

    @api.onchange("person_type")
    def _onchange_person_type(self):
        self._compute_allow_name_edition()

    name = fields.Char(index=True, compute="_compute_name", store=True,
                       readonly=False)

    company_type = fields.Selection(SELECT_COMPANY_TYPES,
                                    string="Company Type")
    person_type = fields.Selection(SELECT_PERSON_TYPES, string="Person Type")

    comment_facts = fields.Text("Facts Comment")
    family_ids = fields.Many2many("res.partner", string="Families",
                                  relation="partner_families",
                                  column1="partner_id",
                                  column2="partner_family_id")
    member_ids = fields.Many2many("res.partner", string="Members",
                                  relation="partner_members",
                                  column1="partner_id",
                                  column2="partner_member_id")

    facts_approved = fields.Boolean()

    is_family = fields.Boolean("Is a family?")

    # For Families
    financial_res_ids = fields.Many2many("res.partner",
                                         string="Financial responsability",
                                         relation="partner_financial_res",
                                         column1="partner_id",
                                         column2="partner_financial_id")

    # Demographics fields
    first_name = fields.Char("First Name")
    middle_name = fields.Char("Middle Name")
    last_name = fields.Char("Last Name")

    date_of_birth = fields.Date(string='Date of birth')
    suffix = fields.Char("Suffix")
    facts_nickname = fields.Char("Facts Nickname")
    ethnicity = fields.Char("Ethnicity")
    facts_citizenship = fields.Char("Facts Citizenship")
    primary_language = fields.Char("Primary Language")
    birth_city = fields.Char("Birth City")
    birth_state = fields.Char("Birth State")
    race = fields.Char("Race")
    gender = fields.Many2one("school_base.gender", string="Gender")

    id_documentation_file = fields.Binary(attachment=True)
    id_documentation_file_name = fields.Char()
    
    passport_id = fields.Char('Passport ID')
    passport_expiration_date = fields.Date('Passport expiration date')
    
    passport_id_file = fields.Binary(attachment=True)
    passport_id_file_name = fields.Char()
    
    residency_permit_id_file = fields.Binary(attachment=True)
    residency_permit_id_file_name = fields.Char()

    medical_allergies_ids = fields.One2many("school_base.medical_allergy", "partner_id", string="Medical Allergies")
    medical_conditions_ids = fields.One2many("school_base.medical_condition", "partner_id", string="Medical conditions")
    medical_medications_ids = fields.One2many("school_base.medical_medication", "partner_id",
                                              string="Medical Medication")

    citizenship = fields.Many2one("res.country", string="Citizenship")
    identification = fields.Char("ID number")
    salutation = fields.Char("Salutation")

    marital_status_id = fields.Many2one('school_base.marital_status', string='Marital status')
    occupation = fields.Char("Occupation")
    title = fields.Char("Title")

    family_member_ids = fields.Many2many(related='family_ids.member_ids')
    relationship_ids = fields.One2many("school_base.relationship", "partner_1", string="Relationships")
    relationship_members_ids = fields.One2many("school_base.relationship", "family_id", string="Relationships Members", readonly=True)

    # Fields for current student status, grade leve, status, etc...
    school_code_id = fields.Many2one('school_base.school_code', string='Current school code')
    grade_level_id = fields.Many2one("school_base.grade_level", string="Grade Level")

    school_year_id = fields.Many2one('school_base.school_year', string="School year", help="The school year where the student is enrolled")

    student_status = fields.Char("Student status (Deprecated)", help="(This field is deprecated)")

    student_status_id = fields.Many2one("school_base.enrollment.status", string="Student status")

    # Fields for next student status, grade leve, status, etc...
    next_school_code_id = fields.Many2one('school_base.school_code', string='Next school code')
    next_grade_level_id = fields.Many2one("school_base.grade_level", string="Next grade level")
    student_next_status_id = fields.Many2one("school_base.enrollment.status", string="Student next status")

    # student_next_status_id = fields.Selection(SELECT_STATUS_TYPES, string="Student next status")
    # student_status_id = fields.Selection(SELECT_STATUS_TYPES, string="Student next status")
    # student_next_status_id2 = fields.Many2one("school_base.enrollment.status", string="Student next status")

    # School information
    home_address_ids = fields.One2many("school_base.home_address", 'family_id', string="Home Addresses",)
    family_home_address_ids = fields.One2many(related='family_ids.home_address_ids', string="Family Home Addresses",)
    home_address_id = fields.Many2one("school_base.home_address", string="Home Address")

    homeroom = fields.Char("Homeroom")
    class_year = fields.Char("Class year")
    student_sub_status_id = fields.Many2one(
        'school_base.enrollment.sub_status', string=_("Sub status"))

    enrolled_date = fields.Date(string=_("Enrolled date"))
    graduation_date = fields.Date(string=_("Graduation date"))

    withdraw_date = fields.Date(string=_("Withdraw date"))
    withdraw_reason_id = fields.Many2one('school_base.withdraw_reason',
                                         string=_("Withdraw reason"))

    reenrollment_record_ids = fields.One2many('school_base.reenrollment.record', 'partner_id')

    reenrollment_status_id = fields.Selection(SELECT_REENROLLMENT_STATUS, string="Reenrollment Status", store=True, compute='_compute_reenrollment_status')
    reenrollment_school_year_id = fields.Many2one('school_base.school_year', string=_("Reenollment school year"), store=True, compute='_compute_reenrollment_status')

    placement_id = fields.Many2one('school_base.placement', string=_("Placement"))

    facts_id_int = fields.Integer("Facts id (Integer)")

    facts_id = fields.Char("Facts id")

    # Facts UDID
    facts_udid_int = fields.Integer("Facts UDID (Integer)", compute="_converts_facts_udid_id_to_int", store=True,
                                    readonly=True)
    facts_udid = fields.Char("Facts UDID")

    # Healthcare
    allergy_ids = fields.One2many("school_base.allergy", "partner_id",
                                  string="Allergies")
    condition_ids = fields.One2many("school_base.condition", "partner_id",
                                    string="Conditions")

    # Enrollment history
    enrollment_history_ids = fields.One2many('school_base.enrollment.history', 'student_id')

    # This fields are mainly used for the onchange method below
    home_address_name = fields.Char(realated='home_address_id.name')
    home_address_country_id = fields.Many2one(realated='home_address_id.country_id')
    home_address_state_id = fields.Many2one(realated='home_address_id.state_id')

    home_address_city = fields.Char(realated='home_address_id.city')
    home_address_zip = fields.Char(realated='home_address_id.zip')
    home_address_street = fields.Char(realated='home_address_id.street')
    home_address_street2 = fields.Char(realated='home_address_id.street2')
    home_address_phone = fields.Char(realated='home_address_id.phone')

    @api.onchange('parent_id', 'home_address_id',
                  'home_address_country_id', 
                  'home_address_state_id',
                  'home_address_city',
                  'home_address_street',
                  'home_address_street2',
                  'home_address_phone',
                  )
    def onchange_parent_id(self):
        res = super(Contact, self).onchange_parent_id()
        res = res or {}
        if self.home_address_id:
            address_fields = self._address_fields()
            if any(self.home_address_id[key] for key in address_fields):
                def convert(value):
                    return value.id if isinstance(value, models.BaseModel) else value
                res['value'] = {key: convert(self.home_address_id[key]) for key in address_fields}
        return res

    @api.onchange('home_address_id', 'home_address_phone')
    def _phone_sync_from_home_address(self):
        for partner in self:
            if partner.home_address_id.phone:
                partner.phone = partner.home_address_id.phone

    def _fields_sync(self, values):
        super(Contact, self)._fields_sync(values)
        if values.get('home_address_id'):
            self._phone_sync_from_home_address()
            onchange_vals = self.onchange_parent_id().get('value', {})
            self.update_address(onchange_vals)

    @api.depends("facts_id")
    def _converts_facts_id_to_int(self):
        for partner_id in self:
            partner_id.facts_id_int = int(partner_id.facts_id) if partner_id.facts_id and partner_id.facts_id.isdigit() else 0

    @api.constrains("facts_id")
    def _check_facts_id(self):
        for partner_id in self:
            if partner_id.facts_id:
                if not partner_id.facts_id.isdigit():
                    raise ValidationError("Facts id needs to be an number")

                should_be_unique = self.search_count([("facts_id", "=", partner_id.facts_id), ('is_family', '=', partner_id.is_family)])
                if should_be_unique > 1:
                    raise ValidationError("Another contact has the same facts id! (%s)" % partner_id.facts_id)
                    
    @api.depends("facts_udid")
    def _converts_facts_udid_id_to_int(self):
        for partner_id in self:
            partner_id.facts_udid_int = int(
                partner_id.facts_udid) if partner_id.facts_udid and partner_id.facts_udid.isdigit() else 0

    @api.constrains("facts_udid")
    def _check_facts_udid_id(self):
        for partner_id in self:
            if partner_id.facts_udid:

                if not partner_id.facts_udid.isdigit():
                    raise ValidationError("Facts id needs to be an number")

                should_be_unique = self.search_count([("facts_id", "=", partner_id.facts_udid)])
                if should_be_unique > 1:
                    raise ValidationError("Another contact has the same facts udid! (%s)" % partner_id.facts_udid)

    @api.depends("facts_udid")
    def _converts_facts_udid_id_to_int(self):
        for partner_id in self:
            partner_id.facts_udid_int = int(
                partner_id.facts_udid) if partner_id.facts_udid and partner_id.facts_udid.isdigit() else 0

    # @api.constrains("facts_udid")
    # def _check_facts_udid_id(self):
    #     for partner_id in self:
    #         if partner_id.facts_udid:
    #
    #             if not partner_id.facts_udid.isdigit():
    #                 raise ValidationError("Facts id needs to be an number")
    #
    #             should_be_unique = self.search_count([("facts_id", "=", partner_id.facts_udid)])
    #             if should_be_unique > 1:
    #                 raise ValidationError("Another contact has the same facts id!")

    @api.model
    def format_name(self, first_name, middle_name, last_name):
        """
        This will format everything depending of school base settings
        :return: A String with the formatted version
        """

        name_order_relation = {
            self.env.ref(
                "school_base.name_sorting_first_name"): first_name or "",
            self.env.ref(
                "school_base.name_sorting_middle_name"): middle_name or "",
            self.env.ref("school_base.name_sorting_last_name"): last_name or ""
            }

        name_sorting_ids = self.env.ref(
            "school_base.name_sorting_first_name") + \
                           self.env.ref(
                               "school_base.name_sorting_middle_name") + \
                           self.env.ref("school_base.name_sorting_last_name")

        name = ""
        sorted_name_sorting_ids = name_sorting_ids.sorted("sequence")
        for sorted_name_id in sorted_name_sorting_ids:
            name += (sorted_name_id.prefix or "") + \
                    name_order_relation.get(sorted_name_id, "") + \
                    (sorted_name_id.sufix or "")

        return name

    def auto_format_name(self):
        """ Use format_name method to create that """
        # partner_ids = self.filtered(lambda partner: partner_id)
        for partner_id in self:
            first = partner_id.first_name
            middle = partner_id.middle_name
            last = partner_id.last_name

            if not partner_id.is_company and not partner_id.is_family and any(
                    [first, middle, last]):
                # old_name = partner_id.name
                partner_id.name = partner_id.format_name(first, middle, last)
            else:
                partner_id.name = partner_id.name

    @api.onchange("first_name", "middle_name", "last_name")
    def _onchange_name_fields(self):
        self.auto_format_name()

    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        self.auto_format_name()

    @api.depends('reenrollment_record_ids')
    def _compute_reenrollment_status(self):
        for partner_id in self:
            reenrollment_record_id = partner_id.reenrollment_record_ids.sorted('create_date', reverse=True)[:1]
            partner_id.reenrollment_school_year_id = reenrollment_record_id.school_year_id.id
            partner_id.reenrollment_status_id = reenrollment_record_id.reenrollment_status

    @api.model
    def create(self, values):
        """ Student custom creation for family relations and other stuffs """

        # Some constant for making more readeable the code
        # ACTION_TYPE = 0
        # TYPE_REPLACE = 6
        TYPE_ADD_EXISTING = 4
        # TYPE_REMOVE_NO_DELETE = 3

        if "name" not in values:
            first_name = values["first_name"] if "first_name" in values else ""
            middle_name = values[
                "first_name"] if "middle_name" in values else ""
            last_name = values["last_name"] if "last_name" in values else ""

            values["name"] = self.format_name(first_name, middle_name,
                                              last_name)
        partners = super().create(values)

        ctx = self._context
        for record in partners:
            if "member_id" in ctx:
                if ctx.get("member_id"):
                    record.write({
                        "member_ids": [
                            [TYPE_ADD_EXISTING, ctx.get("member_id"), False]]
                        })
                else:
                    raise UserError(
                        _("Contact should be save before adding families"))

        return partners

    def write(self, values):
        """ Student custom creation for family relations and other stuffs """

        # Some constant for making more readeable the code
        ACTION_TYPE = 0
        TYPE_REPLACE = 6
        TYPE_ADD_EXISTING = 4
        TYPE_REMOVE_NO_DELETE = 3

        for record in self:
            if "family_ids" in values:
                for m2m_action in values["family_ids"]:
                    if m2m_action[ACTION_TYPE] == TYPE_REPLACE:
                        partner_ids = self.browse(m2m_action[2])
                        removed_parter_ids = self.browse(
                            set(record.family_ids.ids) - set(m2m_action[2]))
                        partner_ids.write({
                            "member_ids": [
                                [TYPE_ADD_EXISTING, record.id, False]],
                            })
                        removed_parter_ids.write({
                            "member_ids": [
                                [TYPE_REMOVE_NO_DELETE, record.id, False]],
                            })

            if "member_ids" in values:
                for m2m_action in values["member_ids"]:
                    if m2m_action[ACTION_TYPE] == TYPE_REPLACE:
                        partner_ids = self.browse(m2m_action[2])
                        removed_parter_ids = self.browse(
                            set(record.family_ids.ids) - set(m2m_action[2]))
                        partner_ids.write({
                            "family_ids": [
                                [TYPE_ADD_EXISTING, record.id, False]],
                            })
                        removed_parter_ids.write({
                            "family_ids": [
                                [TYPE_REMOVE_NO_DELETE, record.id, False]],
                            })

        return super().write(values)

    # Helpers methods
    # devuelve familias de un partner
    def get_families(self):
        PartnerEnv = self.env["res.partner"].sudo()
        return PartnerEnv.search([("is_family", "=", True)]).filtered(
            lambda app: self.id in app.member_ids.ids)
      
    # def recompute_status_id(self):
    #     for partner_id in self.filtered('student_status'):
    #         student_status = partner_id.student_status
    #         if student_status:
    #             for status_name, status_label in SELECT_STATUS_TYPES:
    #                 if student_status.lower() == status_name.lower():
    #                     partner_id.student_status_id = status_name
    #                     break
