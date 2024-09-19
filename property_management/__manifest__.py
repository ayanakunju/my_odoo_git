# -*- coding: utf-8 -*-
{
    'name': "Property Management",
    'version': '17.0.3.0.0',
    'depends': ['base', 'web', 'contacts', 'mail', 'account', 'hr','website'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
   This module gives you a quick view of your property, accessible from your home page.
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/property_management_views.xml',
        'report/lease_management_template.xml',
        'report/lease_management_report.xml',
        'wizard/pdf_message_wizard.xml',
        'views/lease_management_view.xml',
        'views/property_management_menu.xml',
        'views/website_property_management.xml',
        'views/website_template.xml',
        'views/redirect_template.xml',
        'views/property_snippet_template.xml',
        'views/property_templates.xml',
        'data/property_management_sequence.xml',
        'data/property_management_demo.xml',
        'data/email_template.xml',
        'data/lease_expiry_data.xml',
        'data/invoice_payment_followups.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'property_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend':[
            'property_management/static/src/js/dynamic_snippet.js',
            'property_management/static/src/css/website.css',
            'property_management/static/src/xml/property_management_latest_templates.xml',
        ]

    },
    'application': True,
}

