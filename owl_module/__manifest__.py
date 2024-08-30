{
    'name': "Owl Module",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/owl_views.xml',
    ],
   'assets':{
       'web.assets_backend':[
           'owl_module/static/src/js/**',
           'owl_module/static/src/xml/**'
       ]
   },
    # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
    'application': True,
}
