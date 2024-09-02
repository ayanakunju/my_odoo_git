# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    # tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_line_id.tolerance_percentage')

    # @api.onchange('quantity')
    # def onchange_quantity(self):

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for record in self:
            if record.move_ids_without_package:
                sale_order_id =self.env['sale.order'].search([('name', '=' ,self.origin)])
                sale_order =self.env['sale.order'].browse(sale_order_id)

                tolerance = sale_order.order_line.tolerance_percentage
                print(tolerance)

                min_qty = record.move_ids_without_package.quantity - (record.move_ids_without_package.quantity * tolerance / 100)
                max_qty = record.move_ids_without_package.quantity + (record.move_ids_without_package.quantity * tolerance / 100)
                for move in record.move_ids_without_package:
                        if move.quantity < min_qty or move.quantity > max_qty:
                            wizard = self.env['warning.message.wizard'].create({
                                'message': 'Quantity is not acceptable range. Accept or reject?',
                                'accept_button': 'Accept',
                                'reject_button': 'Reject'
                            })
                            if wizard.accept_button:
                                self.quantity = min_qty
                            else:
                                self.quantity = 0

        return res






# class InternalTransfer(models.Model):
#     _inherit = 'stock.picking'
#
#     tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_id.tolerance_percentage')
#
#
#     def calculate_tolerance_range(ordered_qty, tolerance_percentage):
#         min_qty = ordered_qty - (ordered_qty * tolerance_percentage / 100)
#         max_qty = ordered_qty + (ordered_qty * tolerance_percentage / 100)
#         return min_qty, max_qty


# class StockMove(models.Model):
#     _inherit = 'stock.move'
#
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


#  def button_validate(self):
#         res = super().button_validate()
#         for record in self:
#             if record.order_id:
#                 tolerance = record.order_id.partner_id.tolerance_percent
#                 min_qty = record.order_id.order_line.product_uom_qty - (record.order_id.order_line.product_uom_qty * tolerance / 100)
#                 max_qty = record.order_id.order_line.product_uom_qty + (record.order_id.order_line.product_uom_qty * tolerance / 100)
#                 if record.move_lines:
#                     for move in record.move_lines:
#                         if move.product_uom_qty < min_qty or move.product_uom_qty > max_qty:
#                             wizard = self.env['warning.message.wizard'].create({
#                                 'message': 'Quantity is not acceptable range. Accept or reject?',
#                                 'accept_button': 'Accept',
#                                 'reject_button': 'Reject'
#                             })
#                             if wizard.accept_button:
#                                 self.quantity = min_qty
#                             else:
#                                 self.quantity = 0
#         return res