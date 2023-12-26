# -*- coding: utf-8 -*-
{
    'name': "Mobile Shop",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': 'Omar Adel',
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','repair'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/represent.xml',
        'wizard/machine_adjustment.xml',
        'views/repair_order.xml',
        'report/repair_report.xml',
        'report/repair_vendor_report.xml',
        
        
        
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mobile_shop/static/src/css/machine_dashboard.css',
            'mobile_shop/static/src/xml/machine_dashboard.xml',
            'mobile_shop/static/src/js/machine_dashboard.js',
        ],
        
    },
}
