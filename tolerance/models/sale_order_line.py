# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance_percentage = fields.Float(string='Tolerance (%)', default=0)

    @api.onchange('order_id')
    def _onchange_order_id(self):
        if self.order_id:
            self.tolerance_percentage = self.order_id.partner_id.tolerance_percent

    def _prepare_purchase_order_line(self, purchase_order):
        print("function")
        self.ensure_one()
        vals = super(SaleOrderLine, self)._prepare_purchase_order_line(purchase_order)
        vals['tolerance_percentage'] = self.tolerance_percentage
        return vals



    # def _prepare_purchase_order_line(self, order):
    #     res = super(SaleOrderLine, self)._prepare_purchase_order_line(order)
    #     res['tolerance_percentage'] = self.tolerance_percentage
    #     return res

    # def _prepare_purchase_order_line(self, qty,po_id):
    #     res = super(SaleOrderLine, self)._prepare_purchase_order_line(qty,po_id)
    #     res.update({'tolerance_percentage': self.tolerance_percentage, })
    #     # res['tolerance_percentage'] = self.tolerance_percentage
    #     return res


#
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     x_custom_field = fields.Char('Custom Field')
#
# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     x_custom_field = fields.Char('Custom Field')
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     def action_confirm(self):
#         res = super(SaleOrder, self).action_confirm()
#         for order in self:
#             for line in order.order_line:
#                 if line.route_id and line.route_id.mto:
#                     purchase_lines = self.env['purchase.order.line'].search([('sale_line_id', '=', line.id)])
#                     for purchase_line in purchase_lines:
#                         purchase_line.x_custom_field = line.x_custom_field
#         return res

