# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Task",
    'version': '17.0.3.0.0',
    'depends': ['base', 'mrp','stock'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module gives you a view of the total cost of components
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/manufacturing_cost_views.xml',

    ],
    'application': True,
}
