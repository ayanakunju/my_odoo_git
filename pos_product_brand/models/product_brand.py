# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductBrand(models.Model):
    _inherit = 'product.product'

    product_brand = fields.Char(string='Product Brand')
