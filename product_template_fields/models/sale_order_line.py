# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one(related='product_id.brand_id', store=True, string='Product Brand')
    is_prime_customer = fields.Boolean(related='order_partner_id.is_prime_customer', string='Is Prime Customer')


