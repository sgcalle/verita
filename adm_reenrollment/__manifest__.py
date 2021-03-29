# -*- coding: utf-8 -*-
{
    'name': "Admission School Reenrollment",

    'summary': """ Admission School Reenrollment """,

    'description': """ Admission School Reenrollment """,

    'author': "Eduweb Group SL",
    'website': "http://www.eduwebgroup.com",

    'category': 'Admission',
    'version': '0.2',

    'depends': ['adm'],

    'data': [
        'security/ir.model.access.csv',
        'views/adm_reenrollment_views.xml',
        'views/reenrollment_page_views.xml',
        'views/res_config_settings_views.xml',

        'data/email_templates.xml',
        'report/pdf_preview_reports.xml',

        'views/web/portal_templates.xml',

        'views/assets.xml',
        'views/web/templates.xml',

        'data/reenrollment_pages.xml',

        'wizard/create_reenrollment_package.xml',
        'wizard/create_reenrollment_records.xml',

        ],

    'qweb': [
        'static/src/xml/kanban_view_button.xml',
        ],
}
