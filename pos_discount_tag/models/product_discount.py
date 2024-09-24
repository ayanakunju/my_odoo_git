# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductBrand(models.Model):
    _inherit = 'product.product'

    product_discount = fields.Float(string="Discount Tag (%)", help="Product discount tag")
