# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    """ model SaleOrderLine is used to inherit the sale order line and add the custom field tolerance percentage"""
    _inherit = 'sale.order.line'

    tolerance_percentage = fields.Float(string='Tolerance (%)', default=0, help="Tolerance percentage")

    @api.onchange('order_id')
    def _onchange_order_id(self):
        """change the tolerance percentage based on the customer"""
        if self.order_id:
            self.tolerance_percentage = self.order_id.partner_id.tolerance_percent
