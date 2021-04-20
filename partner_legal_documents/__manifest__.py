# -*- coding: utf-8 -*-
{
    'name': "Partner legal documents",

    'summary': """ Documents for partners """,

    'description': """ Documents for partners """,

    'author': "Eduwebgroup SL",
    'website': "http://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    #     ],
}
