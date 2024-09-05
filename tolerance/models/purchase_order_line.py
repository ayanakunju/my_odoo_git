# -*- coding: utf-8 -*-

from odoo import models, fields,api


class PurchaseOrderLine(models.Model):
    """model PurchaseOrderLine is used to inherit the purchase order line and adding the tolerance filed of the
    corresponding sale order line"""
    _inherit = 'purchase.order.line'

    tolerance_percentage = fields.Float(string='Tolerance  (%)',help="tolerance percentage")

    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, company_id,
                                                      values,po):
        """ for adding the tolerance percentage inside the purchase order line"""
        res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, company_id,
                                                                    values, po)
        res['tolerance_percentage'] = values.get('tolerance_percentage', False)
        return res






