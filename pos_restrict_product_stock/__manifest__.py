# -*- coding: utf-8 -*-
{
    'name': 'Display Stock in POS | Restrict Out-of-Stock Products in POS',
    'version': '16.0.1.0.0',
    'category': 'Point of Sale',
    'summary': "Enhance your Point of Sale experience by preventing the "
               "ordering of out-of-stock products during your session",
    'description': "This module enables you to limit the ordering of "
                   "out-of-stock products in POS as well as display the "
                   "available quantity for each product (on-hand quantity "
                   "and virtual quantity).",
    'author': 'Omar Adel',
    'company': 'Company',
    'maintainer': 'Company',
    'website': 'https://www.Company.com',
    'depends': ['point_of_sale'],
    'data': ['views/res_config_settings_views.xml'],
    'assets': {
        'point_of_sale.assets': [
            '/pos_restrict_product_stock/static/src/css/display_stock.css',
            '/pos_restrict_product_stock/static/src/xml/ProductItem.xml',
            '/pos_restrict_product_stock/static/src/xml/RestrictStockPopup.xml',
            '/pos_restrict_product_stock/static/src/js/RestrictStockPopup.js',
            '/pos_restrict_product_stock/static/src/js/ProductScreen.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
