# -*- coding: utf-8 -*-

from odoo import models, fields,api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    tolerance_percentage = fields.Float(string='Tolerance  (%)')

    # @api.model
    # def create(self, vals):
    #     if 'sale_order_line_id' in vals:
    #         sale_order_line = self.env['sale.order.line'].browse(vals['sale_order_line_id'])
    #         vals['tolerance_percentage'] = sale_order_line.tolerance_percentage
    #     return super(PurchaseOrderLine, self).create(vals)

