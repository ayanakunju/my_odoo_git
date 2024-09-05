# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    """stockPicking module is used to inherit the stock picking model for super the button validate
     function inside the sale order"""
    _inherit = 'stock.picking'

    def button_validate(self):
        """when validate the button, based on the product quantity wizard will appear including the accept and
        don't accept button"""
        for record in self:
            if self.env.context.get('validate_from_wizard'):
                return super().button_validate()
            if record.move_ids_without_package:
                sale_order = self.env['sale.order'].search([('name', '=', record.origin)])
                if sale_order:
                    for rec in sale_order.order_line:
                        tolerance = rec.tolerance_percentage
                        for move in record.move_ids_without_package:
                            min_qty = move.product_uom_qty - tolerance
                            max_qty = move.product_uom_qty + tolerance
                            if move.quantity < min_qty or move.quantity > max_qty:
                                return {
                                    'type': 'ir.actions.act_window',
                                    'res_model': 'warning.message.wizard',
                                    'view_mode': 'form',
                                    'view_id': self.env.ref('tolerance.view_warning_message_wizard_form').id,
                                    'target': 'new',
                                    'context': {
                                        'active_id': record.id,
                                        'default_message': 'Quantity is out of the acceptable range.'
                                                           ' Do you want to accept or reject?',
                                        'default_move_id': move.id,
                                    }
                                }
        return super().button_validate()