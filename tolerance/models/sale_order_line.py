# -*- coding: utf-8 -*-


from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance_percentage = fields.Float(string='Tolerance (%)', default=0)

    @api.onchange('order_id')
    def onchange_order_id(self):
        if self.order_id:
            self.tolerance_percentage = self.order_id.partner_id.tolerance_percent



class SaleOrder(models.Model):
    _inherit = 'sale.order'





# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#
#     # tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_line_id.tolerance_percentage')
#
#     @api.onchange('product_uom_qty','quantity')
#     def onchange_quantity(self):
#         for record in self:
#             if record.order_id:
#                 tolerance = record.order_id.partner_id.tolerance_percent
#                 min_qty = record.order_id.order_line.product_uom_qty - (record.order_id.order_line.product_uom_qty * tolerance / 100)
#                 max_qty = record.order_id.order_line.product_uom_qty + (record.order_id.order_line.product_uom_qty * tolerance / 100)
#                 if record.move_lines:
#                     for move in record.move_lines:
#                         if move.product_uom_qty < min_qty or move.product_uom_qty > max_qty:
#                             wizard = self.env['warning.message.wizard'].create({
#                                             'message': 'Quantity is not acceptable range. Accept or reject?',
#                                             'accept_button': 'Accept',
#                                             'reject_button': 'Reject'
#                                         })
#                             if wizard.accept_button:
#                                 self.product_uom_qty = min_qty
#                             else:
#                                 self.product_uom_qty = 0





#
# @api.onchange('order_id')
# def onchange_order_id(self):
#     if self.order_id:
#         self.tolerance_percentage = self.order_id.partner_id.tolerance_percent
#
#
# tolerance_percentage = fields.Float(string='Tolerance (%)', default=0)
#
#
# def action_assign(self):
#     for record in self:
#         if record.order_id:
#             tolerance = record.order_id.partner_id.tolerance_percent
#             min_qty = record.order_id.order_line.product_uom_qty - (
#                         record.order_id.order_line.product_uom_qty * tolerance / 100)
#             max_qty = record.order_id.order_line.product_uom_qty + (
#                         record.order_id.order_line.product_uom_qty * tolerance / 100)
#             if record.move_lines:
#                 for move in record.move_lines:
#                     if move.product_uom_qty < min_qty or move.product_uom_qty > max_qty:
#                         return self.env['warning.wizard'].create({
#                             'message': 'Quantity is out of tolerance range. Please adjust the quantity.',
#                             'accept': 'Accept',
#                             'dont_accept': 'Don\'t Accept'
#                         })
#     return super(StockPicking, self).action_assign()

#
#     def calculate_tolerance_range(ordered_qty, tolerance_percentage):
#         min_qty = ordered_qty - (ordered_qty * tolerance_percentage / 100)
#         max_qty = ordered_qty + (ordered_qty * tolerance_percentage / 100)
#         return min_qty, max_qty


#     @api.onchange('quantity_done')
#     def onchange_quantity_done(self):
#         if self.picking_id.sale_order_id:
#             min_qty, max_qty = calculate_tolerance_range(self.product_uom_qty, self.picking_id.tolerance_percentage)
#         if self.quantity_done < min_qty or self.quantity_done > max_qty:
#             wizard = self.env['warning.message.wizard'].create({
#                 'message': 'Quantity is outside acceptable range. Accept or reject?',
#                 'accept_button': 'Accept',
#                 'reject_button': 'Reject'
#             })
#             if wizard.accept_button:
#                 self.quantity_done = min_qty
#             else:
#                 self.quantity_done = 0


# def action_warning(self):
#    return self.env['warning.wizard'].create({
#      'message': 'Quantity is out of tolerance range. Please adjust the quantity.',
#      'accept': 'Accept',
#      'dont_accept': 'Don\'t Accept'
#    })
