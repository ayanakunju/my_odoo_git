# -*- coding: utf-8 -*-
{
    'name': "Milestone",
    'version': '17.0.3.0.0',
    'depends': ['base', 'sale', 'project'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
        This module gives you a quick view of the milestone of your records
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line_views.xml',

    ],
    'application': True,
}
