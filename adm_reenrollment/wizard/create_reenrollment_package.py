# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime


class CreateReenrollmentPackage(models.TransientModel):
    _name = 'create.reenrollment.package'
    _description = "Reenrollment package"

    def get_default_template(self):

        mail_template_id = \
            self.env['ir.config_parameter']\
                .get_param('adm_reenrollment.reenrollment_announcement_mail_template_id', False)
        mail_template = self.env['mail.template'].browse(int(mail_template_id))
        return mail_template

    name = fields.Char()
    student_ids = fields.Many2many('res.partner')
    already_imported_student_ids = fields.Many2many('res.partner', compute='_compute_already_imported_studets', required=True)
    school_year_id = fields.Many2one('school_base.school_year', default=lambda self: self.env.company.enrollment_school_year_id)
    mail_template_id = fields.Many2one('mail.template', default=get_default_template)

    # This is just for buttons, if you can find a better way just tell me ;-;
    clear_all_button = fields.Boolean()

    @api.onchange('clear_all_button')
    def onchange_clear_all_button(self):
        self.student_ids = False

    @api.onchange('school_year_id')
    def onchange_school_year_id(self):
        for record in self:

            record.already_imported_student_ids = self.env['adm.reenrollment'].search([('school_year_id', '=', record.school_year_id.id)]).mapped('partner_id')

            record.student_ids = self.env['res.partner'].search([
                ('person_type', '=', 'student'),
                ('reenrollment_status_id', '=', 'open'),
                ('reenrollment_school_year_id', '=', record.school_year_id.id),
                ('id', 'not in', record.already_imported_student_ids.ids),
                ])

    @api.model
    def _get_template_partners(self, reenrollment_ids):
        return reenrollment_ids.mapped('custody_user_ids.partner_id')

    def clear_all_students(self):
        self.student_ids = False
        return {"type": False}

    def import_students(self):
        reenrollment_ids = self.env['adm.reenrollment']
        for student in self.student_ids:
            ReenrollmentEnv = self.env['adm.reenrollment']
            reenrollment_id = ReenrollmentEnv.create(self._build_reenrollment_params(student))
            reenrollment_ids += reenrollment_id

        template_partners = self._get_template_partners(reenrollment_ids)
        if template_partners and self.mail_template_id:
            try:
                template_partners.message_post_with_template(template_id=self.mail_template_id.id)
            except:
                pass
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            }

    def _build_reenrollment_params(self, student):
        self.ensure_one()
        stage_id = self.env['adm.reenrollment.stage'].search([('type', '=', 'start')], limit=1, order='sequence')
        if not stage_id:
            stage_id = self.env['adm.reenrollment.stage'].search([], limit=1, order='sequence')
        relationship_custodials = student.self_relationship_ids.filtered(lambda r: r.custody and r.partner_relation_id.email)
        custodials = relationship_custodials.mapped('partner_relation_id')
        # Create users if they doesn't exists
        user_list = []
        for relationship_custodial in relationship_custodials:
            custodial_partner = relationship_custodial.partner_individual_id
            user = self.env['res.users'].sudo().search([('login', '=', custodial_partner.email)])
            if not user:
                # raise Warning("Please enter an email address.")
                x_group_portal_user = self.env.ref('base.group_portal')
                user = self.env['res.users'].with_context(no_reset_password=True).create([{
                     'name': custodial_partner.name,
                     'login': custodial_partner.email,
                     'partner_id': custodial_partner.id,
                     'company_id': self.env.company.id,
                     'groups_id': [
                         (6, 0, [x_group_portal_user.id])],
                    }], )
                # SMTP can fail
                try:
                    user.action_reset_password()
                except:
                    pass

            user_list.append((relationship_custodial, user))

        # responsible_user_id = user_list.pop(0) if user_list else False

        user_access_vals = [(4, 0, {
            'family_id': relationship_custodial.family_id.id,
            'user_id': user.id,
            }) for relationship_custodial, user in user_list]

        return {
            'partner_id': student.id,
            'school_year_id':  self.school_year_id.id,
            'grade_level_id': student.grade_level_id.id,
            'next_grade_level_id': student.next_grade_level_id.id,
            'stage_id': stage_id.id,
            'user_access_ids': user_access_vals,
            }

    def _compute_already_imported_studets(self):
        for record in self:
            record.already_imported_student_ids = self.env['adm.reenrollment'].search([('school_year_id', '=', record.school_year_id.id)]).mapped('partner_id')