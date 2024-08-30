# -*- coding: utf-8 -*-
{
    'name': "Property Management",
    'version': '17.0.3.0.0',
    'depends': ['base', 'contacts', 'mail','account'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module gives you a quick view of your property, accessible from your home page.
    """,

    'data': [
        'security/property_management_groups.xml',
        'security/property_management_security.xml',
        'security/ir.model.access.csv',
        'views/property_management_views.xml',
        'views/lease_management_view.xml',
        'views/property_management_menu.xml',
        'data/property_management_sequence.xml',
        'data/property_management_demo.xml',
        'data/email_template.xml',
        'data/lease_expiry_data.xml',
        'data/invoice_payment_followups.xml',
    ],
    'application': True,
}
