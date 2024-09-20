# -*- coding: utf-8 -*-

{
    'name': "Website Bom",
    'version': '17.0.3.0.0',
    'depends': ['base','website','website_sale','mrp'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module gives you a quick view of your Bom, accessible from your home page.
    """,

    'data': [
        'views/bom_cart_views.xml',
        'views/cart_views.xml',
        ],
    'application': True,

}
