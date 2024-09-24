# -*- coding: utf-8 -*-

{
    'name': "Pos Discount Tag",
    'version': '17.0.3.0.0',
    'depends': ['base','product','point_of_sale'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module add a new field brand in product, and accessible from the pos module.
    """,

    'data': [
            'views/product_discount.xml',
        ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_tag/static/src/js/discount_order_line.js',
            'pos_discount_tag/static/src/xml/discount_order_line.xml',
            'pos_discount_tag/static/src/xml/product_card_inherit.xml',
            'pos_discount_tag/static/src/xml/product_widget_inherit.xml',
            'pos_discount_tag/static/src/css/product_card.css',

        ]
    },
    'application': True,

}
