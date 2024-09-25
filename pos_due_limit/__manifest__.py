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
    #         'pos_discount_tag/static/src/js/discount_order_line.js',
    #         'pos_discount_tag/static/src/xml/discount_order_line.xml',
    #         'pos_discount_tag/static/src/xml/product_card_inherit.xml',
    #         'pos_discount_tag/static/src/xml/product_widget_inherit.xml',
    #         'pos_discount_tag/static/src/css/product_card.css',
        ]
    },
    'application': True,

}
