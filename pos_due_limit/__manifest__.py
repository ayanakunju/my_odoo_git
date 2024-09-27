# -*- coding: utf-8 -*-

{
    'name': "Pos Due Limit",
    'version': '17.0.3.0.0',
    'depends': ['base','contacts','point_of_sale','account'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module set a customer due limit, and accessible from the pos module.
    """,

    'data': [
            'views/due_limit.xml',
        ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_due_limit/static/src/js/pos_due_limit.js',
            'pos_due_limit/static/src/xml/pos_due_limit.xml',
            'pos_due_limit/static/src/css/pos_due_limit.css',

        ]
    },
    'application': True,

}
