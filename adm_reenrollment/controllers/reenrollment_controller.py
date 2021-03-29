# -*- coding: utf-8 -*-

import logging
from odoo import http, exceptions, _
import werkzeug
from datetime import datetime
import base64
import itertools
import re
import json
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response
from odoo.addons.adm.controllers.admission_controller import \
    AdmissionController
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class ReenrollmentController(http.Controller):

    @classmethod
    def is_required(cls, fieldname):
        pass

    @http.route("/my/reenrollments", auth="public", methods=["GET"], website=True)
    def reenrollment_list(self, **params):
        # obtenemos todos los registros de reenrollment en las cuales el
        # estudiante asociado este relacionado mediante la familia con el
        # user que esta accediendo dede el portal.
        reenrollment_ids = request.env.user.reenrollment_ids

        response = http.request.render(
            "adm_reenrollment.template_admission_reenrollment_list", {
                "reenrollment_ids": reenrollment_ids,
                "page_name": 'reenrollments',
                })
        return response

    @http.route("/my/reenrollment/<model(adm.reenrollment):reenrollment_id>", auth="public", methods=["GET"], website=True)
    def reenrollment(self, reenrollment_id, **params):
        # obtenemos todos los registros de reenrollment en las cuales el
        # estudiante asociado este relacionado mediante la familia con el
        # user que esta accediendo dede el portal.
        page_params = self.compute_view_render_params(reenrollment_id)
        response = http.request.render('adm_reenrollment.template_reenrollment_general_info', page_params)
        return response

    @http.route("/my/reenrollment/<model(adm.reenrollment):reenrollment_id>", auth="public", methods=["POST"], csrf=True, type='json')
    def submit_application(self, reenrollment_id, **params):
        self.update_application_with_json(reenrollment_id, **params)

        if reenrollment_id.is_returning:
            returning_stage_id = http.request.env['adm.reenrollment.stage'].sudo().search([('type', '=', 'returning')], limit=1, order='sequence')
            reenrollment_id.sudo().stage_id = returning_stage_id.id
        else:
            not_returning_stage_id = http.request.env['adm.reenrollment.stage'].search([('type', '=', 'not_returning')], limit=1, order='sequence')
            reenrollment_id.sudo().stage_id = not_returning_stage_id.id

        return http.redirect_with_hash("/my/reenrollment/%s" % reenrollment_id.id)

    @http.route("/my/reenrollment/<model(adm.reenrollment):reenrollment_id>", auth="public", methods=["PUT"], csrf=True, type='json')
    def update_application_with_json(self, reenrollment_id, **params):
        """ This is a JSON controller, this get a JSON and write
        the reenrollment with it, that's all
        """

        httprequest = request.httprequest
        json_request = request.jsonrequest

        # if not json_request.get('family_id', False) or reenrollment_id.family_id:
        #     json_request["family_id"] = reenrollment_id.sudo().custody_user_ids.partner_id.family_ids[0].id

        reenrollment_id = reenrollment_id.sudo()
        write_vals = AdmissionController._parse_json_to_odoo_fields(reenrollment_id, json_request)
        reenrollment_id.sudo().write(write_vals)

        user_agent = httprequest.user_agent
        user_agent_vals = {
            'browser': user_agent.browser,
            'language': user_agent.language,
            'platform': user_agent.platform,
            'string': user_agent.string,
            'version': user_agent.version,
            }
        request.env['adm.reenrollment.log'].sudo().create({
            'name': _("Saving changes in reenrollment"),
            'timestamp': datetime.now(),
            'user_id': request.env.user.id,
            'json_values': json.dumps(json_request, indent=4, sort_keys=True),
            'user_agent': json.dumps(user_agent_vals, indent=4, sort_keys=True),
            'ip_address': httprequest.remote_addr,
            'reenrollment_id': reenrollment_id.id,
            })

    @http.route('/my/reenrollment/<model(adm.reenrollment):reenrollment_id>/<path:page_path>',
                methods=["GET"], website=True, strict_slashes=False)
    def generic_page_controller(self, reenrollment_id, page_path, **params):
        page = request.env['adm.reenrollment.page'].search([('url', '=', page_path)])
        page_params = self.compute_view_render_params(reenrollment_id)
        if not page.view_template_id:
            raise werkzeug.exceptions.NotFound()
        page_params.update({
            'page_id': page
            })
        return page.view_template_id.render(page_params)

    @staticmethod
    def compute_view_render_params(reenrollment_id):

        country_ids = request.env['res.country'].search([])
        state_ids = request.env['res.country.state'].search([])

        SUPER_ENV = api.Environment(request.env.cr, SUPERUSER_ID, {})
        reenrollment_id = reenrollment_id.sudo()

        # Binary attachments fields
        # Why not res_field != false ?
        # Well... There can happens some kind of weird bug where just simply
        # changes the name or something...

        attachment_ids = SUPER_ENV['ir.attachment'].search([
            ('res_model', '=', 'adm.reenrollment'),
            ('res_id', '=', reenrollment_id.id),
            ('res_field', '!=', False),
            ])

        field_attachment_ids = {
            field.name: attachment_ids
            .filtered(lambda att: att.res_field == field.name)
            for key, field in reenrollment_id._fields.items()
            if hasattr(field, 'attachment')
            }

        # Testing
        reenrollment_id.regenerate_contract_pdf()

        # field_attachment_ids = SUPER_ENV['ir.attachment'].search([
        #     ('res_field', 'in', attachment_field_name_list),
        #     ('res_model', '=', 'adm.reenrollment'),
        #     ('res_id', '=', reenrollment_id.id)
        #     ])

        guardian_options = \
            reenrollment_id.partner_id.family_ids\
            .mapped('member_ids')\
            .filtered(lambda m: m.person_type != 'student')

        def is_required(fieldname):
            required_fields_name_list =\
                reenrollment_id.get_required_fields().get_as_list_of_names()
            return fieldname in required_fields_name_list

        return {
            "country_ids": country_ids,
            "state_ids": state_ids,
            'reenrollment_id': reenrollment_id,
            'guardian_options': guardian_options,
            'SUPER_ENV': SUPER_ENV,
            'USER_ENV': http.request.env,
            'is_required': is_required,
            'user_family_id': reenrollment_id.current_user_access_id.family_id,
            'field_attachment_ids': field_attachment_ids,
            }