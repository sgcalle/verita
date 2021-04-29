# -*- coding: utf-8 -*-
{
    'name': "Sincro Information from FACTS",

    'summary': """ Tool for the importation from Odoo to FACTS (Applications) """,

    'description': """
        Common models for eduwebgroup school modules
    """,

    'author': "Eduwebgroup",
    'website': "http://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'category': 'Admission',
    'version': '1.0',

    # any module necessary for this one to work correctly, esta acoplado debido a adm debido al wizard
    # se debe desacoplar extrayendo esta funcionalidad en un submodulo
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # Views
        'views/sincro_facts_odoo_res_partner_form.xml',
        'views/sincro_facts_odoo_log_views.xml',

        # Wizard
        # CSS
    ],
    'qweb': [],
    'demo': []
}
