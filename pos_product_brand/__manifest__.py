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
    'application': True,

}
