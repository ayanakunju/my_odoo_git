# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    """ model SaleOrderLine is used to inherit the sale order line """
    _inherit = 'sale.order.line'


    @api.depends('order_id')
    def get_ordered_quantites(self):
        # products = self.env['product.template'].search([('product_id.invoice_policy', '=', 'order')])
        products = self.env['product.template'].search([]).filtered(
                                lambda x: self.order_id.partner_id in x.item_ids.mapped('invoice_policy','=','order'))
        product_ids = self.env['product.product'].search([('product_id','in', products)])
        if self.order_id.partner_id.is_only_ordered == "True":
            self.order_id.product_id = products

            return{'domain': {'product_id':[('id','in', product_ids)]}}

