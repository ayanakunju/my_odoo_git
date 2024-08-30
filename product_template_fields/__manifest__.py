# -*- coding: utf-8 -*-
{
    'name': "Product Template Fields",
    'version': '17.0.3.0.0',
    'depends': ['base', 'product','sale','contacts'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module gives you a quick view of the brand of your products
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_template_menu.xml',
        'views/sale_order_line_views.xml'
    ],
    'application': True,
}
