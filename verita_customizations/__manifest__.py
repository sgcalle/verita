# -*- coding: utf-8 -*-
{
    'name': "Verita customizations",

    'summary': """ Verita customizations """,

    'description': """""",

    'author': "Eduwegroup",
    'website': "https://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': [
        'adm',
        'adm_reenrollment',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        ],
}
