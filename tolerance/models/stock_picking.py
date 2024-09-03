# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        for record in self:
            if record.move_ids_without_package:
                sale_order = self.env['sale.order'].search([('name', '=', record.origin)])
                print(sale_order)
                if sale_order:
                    for rec in sale_order.order_line:
                        tolerance = rec.tolerance_percentage
                        print(tolerance)
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
                                        'default_message': 'Quantity is out of the acceptable range. Do you want to accept or reject?',
                                        'default_move_id': move.id,
                                    }
                                }

        return res

    # class StockPicking(models.Model):
    #     _inherit = 'stock.picking'
    #
    #     def button_validate(self):
    #         res = super(StockPicking, self).button_validate()
    #         for record in self:
    #             if record.move_ids_without_package:
    #                 sale_order = self.env['sale.order'].search([('name', '=', record.origin)], limit=1)
    #                 if sale_order:
    #                     tolerance = sale_order.order_line.tolerance_percentage
    #                     for move in record.move_ids_without_package:
    #                         min_qty = move.product_uom_qty - tolerance
    #                         max_qty = move.product_uom_qty + tolerance
    #                         if move.quantity < min_qty or move.quantity > max_qty:
    #                             return {
    #                                 'type': 'ir.actions.act_window',
    #                                 'res_model': 'warning.message.wizard',
    #                                 'view_mode': 'form',
    #                                 'view_id': self.env.ref('tolerance.view_warning_message_wizard_form').id,
    #                                 'target': 'new',
    #                                 'context': {
    #                                     'default_message': 'Quantity is out of the acceptable range. Do you want to accept or reject?',
    #                                     'default_accept_button': 'Accept',
    #                                     'default_reject_button': 'Reject',
    #                                     'default_move_id': move.id,
    #                                 }
    #                             }
    #         return res
    #











    #     # tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_line_id.tolerance_percentage')
    #     # @api.onchange('quantity')
    #     # def onchange_quantity(self):
    #
    #     # def button_validate(self):
    #     #     res = super(StockPicking, self).button_validate()
    #     #     for record in self:
    #     #         if record.move_ids_without_package:
    #     #             sale_order_id =self.env['sale.order'].search([('name', '=' ,self.origin)])
    #     #             sale_order =self.env['sale.order'].browse(sale_order_id)
    #     #
    #     #             tolerance = sale_order.order_line.tolerance_percentage
    #     #             print(tolerance)
    #     #
    #     #             min_qty = record.move_ids_without_package.quantity - (record.move_ids_without_package.quantity * tolerance / 100)
    #     #             max_qty = record.move_ids_without_package.quantity + (record.move_ids_without_package.quantity * tolerance / 100)
    #     #             for move in record.move_ids_without_package:
    #     #                     if move.quantity < min_qty or move.quantity > max_qty:
    #     #                         wizard = self.env['warning.message.wizard'].create({
    #     #                             'message': 'Quantity is not acceptable range. Accept or reject?',
    #     #                             'accept_button': 'Accept',
    #     #                             'reject_button': 'Reject'
    #     #                         })
    #     #                         if wizard.accept_button:
    #     #                             self.quantity = min_qty
    #     #                         else:
    #     #                             self.quantity = 0
    #     #
    #     #     return res

    # tolerance_percentage = fields.Float(string='Tolerance Percentage', related='sale_order_line_id.tolerance_percentage')
    # @api.onchange('quantity')
    # def onchange_quantity(self):

    # def button_validate(self):
    #     res = super(StockPicking, self).button_validate()
    #     for record in self:
    #         if record.move_ids_without_package:
    #             sale_order_id =self.env['sale.order'].search([('name', '=' ,self.origin)])
    #             sale_order =self.env['sale.order'].browse(sale_order_id)
    #
    #             tolerance = sale_order.order_line.tolerance_percentage
    #             print(tolerance)
    #
    #             min_qty = record.move_ids_without_package.quantity - (record.move_ids_without_package.quantity * tolerance / 100)
    #             max_qty = record.move_ids_without_package.quantity + (record.move_ids_without_package.quantity * tolerance / 100)
    #             for move in record.move_ids_without_package:
    #                     if move.quantity < min_qty or move.quantity > max_qty:
    #                         wizard = self.env['warning.message.wizard'].create({
    #                             'message': 'Quantity is not acceptable range. Accept or reject?',
    #                             'accept_button': 'Accept',
    #                             'reject_button': 'Reject'
    #                         })
    #                         if wizard.accept_button:
    #                             self.quantity = min_qty
    #                         else:
    #                             self.quantity = 0
    #
    #     return res

#  def button_validate(self):
#         res = super(StockPicking, self).button_validate()
#         for record in self:
#             if record.move_ids_without_package:
#                 # Fetch the related sale order based on the origin field
#                 sale_order = self.env['sale.order'].search([('name', '=', record.origin)], limit=1)
#                 if sale_order:
#                     tolerance = sale_order.order_line.tolerance_percentage
#                     for move in record.move_ids_without_package:
#                         min_qty = move.product_uom_qty - (move.product_uom_qty * tolerance / 100)
#                         max_qty = move.product_uom_qty + (move.product_uom_qty * tolerance / 100)
#
#                         if move.quantity < min_qty or move.quantity > max_qty:
#                             # Open the warning wizard if quantity is out of tolerance range
#                             return {
#                                 'type': 'ir.actions.act_window',
#                                 'res_model': 'warning.message.wizard',
#                                 'view_mode': 'form',
#                                 'view_id': self.env.ref('my_module.view_warning_message_wizard_form').id,
#                                 'target': 'new',
#                                 'context': {
#                                     'default_message': 'Quantity is out of the acceptable range. Do you want to accept or reject?',
#                                     'default_accept_button': 'Accept',
#                                     'default_reject_button': 'Reject',
#                                     'default_move_id': move.id,
#                                 }
#                             }
#         return res
#        # return super(StockPicking, self).button_validate()

#
#
# class WarningMessageWizard(models.TransientModel):
#     _name = 'warning.message.wizard'
#     _description = 'Warning Message Wizard'
#
#     message = fields.Text('Message', readonly=True)
#     accept_button = fields.Selection([
#         ('accept', 'Accept'),
#         ('reject', 'Reject')
#     ], string='Action', required=True)
#     move_id = fields.Many2one('stock.move', 'Stock Move', required=True)
#
#     def action_confirm(self):
#         move = self.move_id
#         tolerance = self.env['sale.order'].search([('name', '=', move.picking_id.origin)], limit=1).order_line.tolerance_percentage
#         min_qty = move.product_uom_qty - (move.product_uom_qty * tolerance / 100)
#         max_qty = move.product_uom_qty + (move.product_uom_qty * tolerance / 100)
#
#         if self.accept_button == 'accept':
#             move.write({'quantity_done': min_qty})
#         else:
#             move.write({'quantity_done': 0})
#
#         return {'type': 'ir.actions.act_window_close'}
#
# <!-- -->
# <odoo>
#     <record id="view_warning_message_wizard_form" model="ir.ui.view">
#         <field name="name">warning.message.wizard.form</field>
#         <field name="model">warning.message.wizard</field>
#         <field name="arch" type="xml">
#             <form string="Warning Message">
#                 <header>
#                     <button string="Accept" type="object" name="action_confirm" class="btn-primary"/>
#                     <button string="Reject" type="object" name="action_confirm" class="btn-secondary"/>
#                 </header>
#                 <sheet>
#                     <field name="message" readonly="1"/>
#                 </sheet>
#             </form>
#         </field>
#     </record>
# </odoo>


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
