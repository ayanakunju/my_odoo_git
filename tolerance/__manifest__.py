# -*- coding: utf-8 -*-
{
    'name': "Tolerance",
    'version': '17.0.3.0.0',
    'depends': ['base', 'sale', 'contacts', 'stock', 'purchase'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
        This module gives you a quick view of the tolerance of your orders
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_line_views.xml',
        'views/purchase_order_line_views.xml',
        'views/warning_message_wizard.xml',
    ],
    'application': True,
}
