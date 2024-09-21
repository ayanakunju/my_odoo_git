# -*- coding: utf-8 -*-

from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Char(string='Product Brand')
