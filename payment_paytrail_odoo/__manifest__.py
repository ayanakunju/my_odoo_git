# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: Paytrail',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'description': " payment provider for online payments all over the world ",
    'author': 'Odoo',
    'depends': ['payment'],
    'data': [
        'views/payment_paytrail_template.xml',
        'views/payment_provider_views.xml',

        # 'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],

    'license': 'LGPL-3'
}
