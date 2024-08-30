# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Product Brand')
    product_master_type = fields.Selection(selection=[('single_product', 'Single Product'), ('branded_product', 'Branded Product')],
                                           string='Product Master Type', required=True, copy=False, tracking=True, default='single_product')
