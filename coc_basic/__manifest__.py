# -*- coding: utf-8 -*-
{
    'name': "Cocc Basic",
    'version': '1.0',
    'depends': ['base','mrp'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module gives you a quick view of your property, accessible from your home page.
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/coc_basic.xml',
    #     'views/lease_management_view.xml',
    #     'views/property_management_menu.xml',
    #     'data/property_management_sequence.xml',
    #     'data/property_management_demo.xml',
    ],
    'application': True,
}
