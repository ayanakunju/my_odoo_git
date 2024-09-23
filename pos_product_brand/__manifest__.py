# -*- coding: utf-8 -*-

{
    'name': "Pos Product Brand",
    'version': '17.0.3.0.0',
    'depends': ['base','product','point_of_sale'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module add a new field brand in product, and accessible from the pos module.
    """,

    'data': [
            'views/product_brand.xml',
        ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_brand/static/src/js/pos_order_line.js',
            'pos_product_brand/static/src/xml/pos_order_line.xml',
            'pos_product_brand/static/src/xml/product_info.xml',
        ]
    },
    'application': True,

}
