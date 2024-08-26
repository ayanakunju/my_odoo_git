{
    'name': "hospital_management",
    'version': '1.0',
    'depends': ['base','contacts','hr'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    # 'data': [
    #     'views/mymodule_view.xml',
    # ],
    'data':[
        'security/ir.model.access.csv',
        'views/hospital_views.xml',
        'views/op_model.xml',
        'views/consultation_model.xml',
        'data/opticket_sequence.xml',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
    'application': True,
}
