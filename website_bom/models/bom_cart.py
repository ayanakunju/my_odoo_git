
# -*- coding: utf-8 -*-

from odoo import api, fields , models
from ast import literal_eval


class BomCart(models.TransientModel):
    _inherit = 'res.config.settings'

    is_bom_product = fields.Boolean(string="Products BOM", config_parameter='website_bom.bom_cart', default=False)
    product_ids = fields.Many2many('product.product',string='Products')


    @api.model
    def get_values(self):
        """ it returns the saved values when loading the website"""
        res = super(BomCart, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        products = with_user.get_param('website_bom.bom_cart')
        res.update(product_ids=[fields.Command.set(literal_eval(products))
                                ] if products else False, )
        return res


    def set_values(self):
        """stores the saved values of the config parameters"""
        res = super(BomCart, self).set_values()
        if self.is_bom_product:
                self.env['ir.config_parameter'].sudo().set_param(
                'website_bom.bom_cart', self.product_ids.ids)
        return res
