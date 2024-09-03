# -*- coding: utf-8 -*-
from odoo import models, fields


class WarningMessageWizard(models.TransientModel):
    _name = 'warning.message.wizard'
    _description = 'Warning Message Wizard'

    message = fields.Text(string="Quantity is out of the acceptable range. Do you want to accept or reject?")
    default_accept_button = fields.Char(string='Accept Button')
    default_reject_button = fields.Char(string='Reject Button')
    default_move_ids = fields.Many2many('stock.move', string='Moves')


    def action_accept(self):
        active = self._context.get('active_ids')
        print(active)
        for move in self.default_move_ids:
            move.picking_id.button_validate()
        return {'type': 'ir.actions.act_window_close'}


    def action_reject(self):
        active = self._context.get('active_ids')
        active_id = self.env['sale.order'].browse['active_ids']
        print(active_id)
        active_id.write({
            'state': "cancel"
})
        return {'type': 'ir.actions.act_window_close'}



 # def action_confirm(self):
 #        res = super(SaleOrder, self).action_confirm()
 #        for order in self:
 #            for line in order.order_line:
 #                if line.tolerance_percentage:
 #                    purchase_orders = line.purchase_order_ids
 #                    for rec in purchase_orders:
 #                        for rec_line in rec.order_line:
 #                            if rec_line.product_id == line.product_id:
 #                                rec_line.tolerance_percentage = line.tolerance_percentage
 #        return res





# class WarningMessageWizard(models.TransientModel):
#     _name = 'warning.message.wizard'
#     _description = 'Warning Message Wizard'
#
#     message = fields.Text('Message', readonly=True)
#     accept_button = fields.Selection([('accept', 'Accept'),('reject', 'Reject')], string='Action', required=True)
#     move_id = fields.Many2one('stock.move', 'Stock Move', required=True)
#
#
#     def action_confirm(self):
#         move = self.move_id
#         tolerance = self.env['sale.order'].search([('name', '=', move.picking_id.origin)], limit=1).order_line.tolerance_percentage
#         min_qty = move.product_uom_qty - (move.product_uom_qty * tolerance / 100)
#         max_qty = move.product_uom_qty + (move.product_uom_qty * tolerance / 100)
#
#         if self.accept_button == 'accept':
#             move.write({'quantity_done': min_qty})
#             return {'type': 'ir.actions.act_window_close'}
#         else:
#            return {'type' : 'ir.actions.act_window',
#             'res_model': 'warning.message.wizard',
#             'view_mode': 'form',
#             'view_id': self.env.ref('tolerance.view_warning_message_wizard_form').id,
#             'target': 'new',
#             'context': {
#                 'default_message': 'Quantity is out of the acceptable range. Do you want to accept or reject?',
#                 'default_accept_button': 'Accept',
#                 'default_reject_button': 'Reject',
#                 'default_move_id': move.id,
#             }
#                    }
#
#
#
#
#         #     move.write({'quantity_done': 0})
#         # return {'type': 'ir.actions.act_window_close'}


# class WarningMessageWizard(models.TransientModel):
#     _name = 'warning.message.wizard'
#     _description = 'Warning Message Wizard'
#
#
#     # message = fields.Char(string='Message')
#     # # accept_button = fields.Boolean(string='Accept')
#     # # reject_button = fields.Boolean(string='Reject')
#     # accept_button = fields.Selection([('accept', 'Accept'),('reject', 'Reject')], string='Action', required=True)
#     #
#     # def accept(self):
#     #     return {'type': 'ir.actions.act_window_close'}
#     #
#     # def reject(self):
#     #     return {'type': 'ir.actions.act_window_close'}